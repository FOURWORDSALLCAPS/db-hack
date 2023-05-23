from datacenter.models import *
from django.core.exceptions import ObjectDoesNotExist
import random


def fix_marks(schoolkid):
    marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
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


def create_commendation(schoolkid, subject):
    commendations = ['Молодец!', 'Ты меня очень обрадовал!', 'Хорошо!',
                     'Хвалю!', 'Великолепно!', 'Замечательно!',
                     'Я тобой горжусь!', 'Сказано здорово – просто и ясно!', 'Потрясающе!',
                     'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
                     'Теперь у тебя точно все получится!', ' Очень хороший ответ!', 'Талантливо!'
                     ]
    commendation = random.choice(commendations)
    teacher_name = Lesson.objects.filter(
        subject=subject,
        group_letter__contains='А'
    ).first().teacher.full_name
    teacher = Teacher.objects.filter(full_name__contains=f"{teacher_name}").first()
    date_last_lesson = Lesson.objects.exclude(
        year_of_study__contains="6",
        group_letter__contains="А",
        subject__title__contains=subject
    ).order_by('-date').first().date
    Commendation.objects.create(
        text=commendation,
        created=f"{date_last_lesson}",
        schoolkid=schoolkid,
        subject=subject,
        teacher=teacher
    )


def main():
    child = 'Фролов Иван'
    subject = 'Математика'
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=f"{child}")
        subject = Subject.objects.get(year_of_study__contains="6", title__contains=f"{subject}")
    except ObjectDoesNotExist:
        print("Either the entry or blog doesn't exist.")


if __name__ == '__main__':
    main()
