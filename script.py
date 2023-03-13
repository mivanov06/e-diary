from django.core import exceptions

from datacenter.models import Schoolkid, Mark, Commendation, Lesson, Subject, Chastisement

from random import choice

COMMENDATIONS = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Прекрасное начало!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!",
]


def get_schoolkid(schoolkid_name: str):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.MultipleObjectsReturned:
        print(f'Найдено несколько учеников с именем {schoolkid_name}. Повторите поиск')
    except Schoolkid.DoesNotExist:
        print(f'Ученик с таким именем {schoolkid_name} не найден. Повторите поиск')


def fix_marks(schoolkid: Schoolkid):
    if schoolkid is not None:
        Mark.objects.filter(schoolkid=schoolkid.id, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid: Schoolkid):
    if schoolkid is not None:
        Chastisement.objects.filter(schoolkid=schoolkid).delete()


def get_subject(lesson_name: str, schoolkid: Schoolkid):
    try:
        return Subject.objects.get(title=lesson_name, year_of_study=schoolkid.year_of_study)
    except Subject.MultipleObjectsReturned:
        print(f"Много совпадений по названию предмета {lesson_name}. Уточните предмет")
    except Subject.DoesNotExist:
        print(f"Предмет {lesson_name} не найден. Повторит запрос")


def create_commendation(lesson_name: str, schoolkid_name: str):
    schoolkid = get_schoolkid(schoolkid_name)
    if schoolkid is not None:
        subject = get_subject(lesson_name, schoolkid)
        if subject is not None:
            lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                            subject=subject)
            if lessons is not None:
                lesson = choice(lessons)
                commendation = Commendation.objects.create(text=choice(COMMENDATIONS), created=lesson.date,
                                                           schoolkid=schoolkid,
                                                           subject=lesson.subject, teacher=lesson.teacher)
                return commendation
            else:
                return f'Не найдено занятий по предмету {subject.title}'
