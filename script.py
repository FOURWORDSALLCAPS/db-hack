from datacenter.models import Teacher
from datacenter.models import Mark
from datacenter.models import Subject
from datacenter.models import Commendation
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Schoolkid
import random

COMMENDATION = ['Молодец!', 'Ты меня очень обрадовал!', 'Хорошо!',
                'Хвалю!', 'Великолепно!', 'Замечательно!',
                'Я тобой горжусь!', 'Сказано здорово – просто и ясно!', 'Потрясающе!',
                'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
                'Теперь у тебя точно все получится!', ' Очень хороший ответ!', 'Талантливо!'
                ]


def get_schoolkid(child):
    try:
        return Schoolkid.objects.get(full_name__contains=child)
    except Schoolkid.MultipleObjectsReturned:
        print("There are several such schoolkids.")
    except ObjectDoesNotExist:
        print("Schoolkid matching query does not exist.")


def fix_marks(child):
    schoolkid = get_schoolkid(child)
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(child):
    schoolkid = get_schoolkid(child)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(child, subject):
    schoolkid = get_schoolkid(child)
    try:
        subject = Subject.objects.get(year_of_study__contains="6", title__contains=subject)
        commendation = random.choice(commendations)
        teacher_name = Lesson.objects.filter(
            subject=subject,
        ).first().teacher.full_name
        date_last_lesson = Lesson.objects.exclude(
            subject__title__contains=subject
        ).order_by('-date').first().date
        teacher = Teacher.objects.filter(full_name__contains=teacher_name).first()
        Commendation.objects.create(
            text=commendation,
            created=f"{date_last_lesson}",
            schoolkid=schoolkid,
            subject=subject,
            teacher=teacher
        )
    except MultipleObjectsReturned:
        print("There are several such subject.")
    except Subject.DoesNotExist:
        print("Subject matching query does not exist.")
