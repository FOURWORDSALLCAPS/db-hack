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
        return None
    except Schoolkid.DoesNotExist:
        print("Schoolkid matching query does not exist.")
        return None


def fix_marks(child):
    schoolkid = get_schoolkid(child)
    if schoolkid is not None:
        Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(child):
    schoolkid = get_schoolkid(child)
    if schoolkid is not None:
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        chastisements.delete()


def create_commendation(child, subject):
    schoolkid = get_schoolkid(child)
    try:
        subject = Subject.objects.get(year_of_study__contains="6", title__contains=subject)
        commendation = random.choice(COMMENDATION)
        teacher_name = Lesson.objects.filter(
            subject=subject,
        ).first()
        if teacher_name is not None:
            teacher_name = teacher_name.teacher.full_name
        date_last_lesson = Lesson.objects.exclude(
            subject__title__contains=subject
        ).order_by('-date').first()
        teacher = Teacher.objects.filter(full_name__contains=teacher_name).first()
        if date_last_lesson is not None:
            date_last_lesson = date_last_lesson.date
        if schoolkid is not None:
            Commendation.objects.create(
                text=commendation,
                created=f"{date_last_lesson}",
                schoolkid=schoolkid,
                subject=subject,
                teacher=teacher
            )
    except Subject.MultipleObjectsReturned:
        print("There are several such subject.")
    except Subject.DoesNotExist:
        print("Subject matching query does not exist.")
