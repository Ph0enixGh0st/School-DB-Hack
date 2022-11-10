import random
import sys

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datacenter.models import Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject

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


def fix_marks(child):
	Mark.objects.filter(schoolkid_id=child.id, points__lt=4).update(points=5)


def remove_chastisements(child):
	Chastisement.objects.filter(schoolkid_id=child.id).delete()


def create_commendation(child, school_subject, random_appraisal):

	lesson = Subject.objects.get(title=school_subject, year_of_study=child.year_of_study)
	lessons_pool = Lesson.objects.filter(year_of_study=child.year_of_study, 
                                            group_letter=child.group_letter, 
                                            subject__title=lesson).order_by('-date')

	Commendation.objects.create(text=random_appraisal, created=lessons_pool.date, 
                                schoolkid_id=child.id, subject=lessons_pool.subject, 
                                teacher=lessons_pool.teacher)


def main():

	parser = argparse.ArgumentParser(description="The script hacks the school database")
	parser.add_argument("-n", "--name", default="", help="Enter full name here", type=str)
	parser.add_argument("-d", "--discipline", default="", help="Enter school subject here", type=str)
	args = parser.parse_args()
	name = args.name
	school_subject = args.discipline

	if not name:
		print("Empty name provided")
	try:
		child = Schoolkid.objects.get(full_name__contains=name)
	except Schoolkid.MultipleObjectsReturned:
		print("There are multiple IDs with provided name.")
	except Schoolkid.ObjectDoesNotExist:
		print("Schoolkid entry doesn't exist in database.")

	if not school_subject:
		print("Empty school_subject provided")
	try:
        	school_subject = Subject.objects.get(title=school_subject, year_of_study=child.year_of_study)
    	except Subject.ObjectDoesNotExist:
        	print(f"{school_subject} not found")  

    fix_marks(child)
    remove_chastisements(child)
    create_commendation(child, school_subject, random_appraisal)


if __name__ == '__main__':
    main()
