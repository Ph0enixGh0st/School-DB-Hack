import random
import sys

import django.core.exceptions
from datacenter.models import Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject


def fix_marks(child):
	Mark.objects.filter(schoolkid=child, points__lt=4).update(points=5)


def remove_chastisements(child):
	Chastisement.objects.filter(schoolkid=child).delete()


def create_commendation(child, subject):

    appraisals = [
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
        "Теперь у тебя точно все получится!"
        ]
    
    random_appraisal = random.choice(appraisals)
    lesson = Subject.objects.get(title=subject, year_of_study=child.year_of_study)
    last_lesson_pick = Lesson.objects.filter(year_of_study=child.year_of_study, group_letter=child.group_letter, subject__title=lesson).order_by('-date')
    Commendation.objects.create(text=random_appraisal, created=last_lesson_pick.date, schoolkid=child, subject=last_lesson_pick.subject, teacher=last_lesson_pick.teacher)


def main():

    parser = argparse.ArgumentParser(description="The script hacks the school database")
    parser.add_argument("-n", "--name", default="", help="Enter full name here", type=str)
    parser.add_argument("-s", "--subject", default="", help="Enter subject here", type=str)
    args = parser.parse_args()
    name = args.name
    subject = args.subject

    if not name:
        print("Empty name provided")
    try:
        child = Schoolkid.objects.get(full_name__contains=name)
    except django.core.exceptions.MultipleObjectsReturned:
        print("There are multiple IDs with provided name.")
    except django.core.exceptions.ObjectDoesNotExist:
        print("Schoolkid entry doesn't exist in database.")

    if not subject:
        print("Empty subject provided")
    try:
        subject = Subject.objects.get(title=subject, year_of_study=child.year_of_study)
    except django.core.exceptions.ObjectDoesNotExist:
        print(f"{subject} not found")
    
    fix_marks(child)
    remove_chastisements(child)
    create_commendation(child, subject)


if __name__ == '__main__':
    main()
