from datacenter.models import Teacher
from datacenter.models import Mark
from datacenter.models import Subject
from datacenter.models import Commendation
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Schoolkid
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random


commendations = ['Молодец!', 'Ты меня очень обрадовал!', 'Хорошо!',
                 'Хвалю!', 'Великолепно!', 'Замечательно!',
                 'Я тобой горжусь!', 'Сказано здорово – просто и ясно!', 'Потрясающе!',
                 'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
                 'Теперь у тебя точно все получится!', ' Очень хороший ответ!', 'Талантливо!'
                 ]


def fix_marks(child):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=child)
        Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)
    except MultipleObjectsReturned:
        print("There are several such schoolkids.")
    except ObjectDoesNotExist:
        print("Schoolkid matching query does not exist.")


def remove_chastisements(child):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=child)
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        chastisements.delete()
    except MultipleObjectsReturned:
        print("There are several such schoolkids.")
    except ObjectDoesNotExist:
        print("Schoolkid matching query does not exist.")


def remove_commendation(child):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=child)
        commendation = Commendation.objects.filter(schoolkid=schoolkid)
        commendation.delete()
    except MultipleObjectsReturned:
        print("There are several such schoolkids.")
    except ObjectDoesNotExist:
        print("Schoolkid matching query does not exist.")


def create_commendation(child, subject):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=child)
        subject = Subject.objects.get(year_of_study__contains="6", title__contains=subject)
        commendation = random.choice(commendations)
        teacher_name = Lesson.objects.filter(
            subject='subject',
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
        print("There are several such schoolkids.")
    except ObjectDoesNotExist:
        print("Either the schoolkid or subject does not exist.")
