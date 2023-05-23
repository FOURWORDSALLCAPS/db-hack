from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Teacher
from datacenter.models import Subject
from django.core.exceptions import ObjectDoesNotExist
import random


def fix_marks(schoolkid):
    for child in schoolkid:
        marks = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
        for mark in marks:
            mark.points = 5
            mark.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in chastisements:
        chastisement.delete()


def remove_commendation(schoolkid):
    commendations = Commendation.objects.filter(schoolkid=schoolkid)
    for commendation in commendations:
        commendation.delete()


def create_commendation(schoolkid, lesson):
    commendations = ['Молодец!', 'Ты меня очень обрадовал!', 'Хорошо!',
                     'Хвалю!', 'Великолепно!', 'Замечательно!',
                     'Я тобой горжусь!', 'Сказано здорово – просто и ясно!', 'Потрясающе!',
                     'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
                     'Теперь у тебя точно все получится!', ' Очень хороший ответ!', 'Талантливо!'
                     ]
    commendation = random.choice(commendations)
    subject = Subject.objects.filter(
        year_of_study__contains="6",
        title__contains=f"{lesson}"
    ).first()
    teacher_name = Lesson.objects.filter(
        year_of_study__contains="6",
        group_letter__contains="А",
        subject__title=f'{lesson}'
    ).first().teacher.full_name
    teacher = Teacher.objects.filter(full_name__contains=f"{teacher_name}").first()
    date_last_lesson = Lesson.objects.exclude(
        year_of_study__contains="6",
        group_letter__contains="А",
        subject__title__contains=f"{lesson}",
    ).order_by('-date').first().date
    Commendation.objects.create(
        text=commendation,
        created=f"{date_last_lesson}",
        schoolkid=schoolkid,
        subject=subject,
        teacher=teacher
    )


def main():
    child = "Фролов Иван"
    lesson = 'Музыка'
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=f"{child}")
    except ObjectDoesNotExist:
        print("Either the entry or blog doesn't exist.")


if __name__ == '__main__':
    main()
