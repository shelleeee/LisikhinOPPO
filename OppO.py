import re
import datetime

# Класс Lesson представляет собой занятие с датой, номером комнаты и именем преподавателя
class Lesson:
    def __init__(self, date: datetime.date, room: str, teacher: str) -> None:
        self.date = date  # Дата занятия
        self.room = room  # Номер комнаты
        self.teacher = teacher  # Имя преподавателя с отчеством

# Класс LessonParser содержит статические методы для извлечения данных из строки
class LessonParser:
    @staticmethod
    def extract_date(line: str) -> datetime.date:
        try:
            date_str = re.findall(r"\d{4}\.\d{2}\.\d{2}", line)[0]
            return datetime.datetime.strptime(date_str, "%Y.%m.%d").date()
        except IndexError:
            raise ValueError("Неверный формат даты")

    @staticmethod
    def extract_room(line: str) -> str:
        try:
            return re.findall(r"\d-\d{2}", line)[0]
        except IndexError:
            raise ValueError("Неверный формат комнаты")

    @staticmethod
    def extract_teacher(line: str) -> str:
        try:
            return re.findall(r'"(.+?)"', line)[0]
        except IndexError:
            raise ValueError("Неверный формат преподавателя")

def read(txt_file: str) -> list:
    result = []
    try:
        with open(txt_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                date = LessonParser.extract_date(line)
                room = LessonParser.extract_room(line)
                teacher = LessonParser.extract_teacher(line)
                new_lesson = Lesson(date, room, teacher)
                result.append(new_lesson)
    except FileNotFoundError:
        raise FileNotFoundError("Файл не существует")
    return result

def filter_lessons(lessons: list, find_teacher: str = None, find_room: str = None, find_date: str = None) -> list:
    filtered_lessons = []
    for lesson in lessons:
        # Проверяем, соответствует ли занятие заданным параметрам
        if (not find_teacher or find_teacher.lower() in lesson.teacher.lower()) and \
           (not find_room or find_room.lower() in lesson.room.lower()) and \
           (not find_date or LessonParser.extract_date(find_date) == lesson.date):
            # Если занятие соответствует всем параметрам, добавляем его в список отфильтрованных занятий
            filtered_lessons.append(lesson)
    return filtered_lessons

def show(lessons: list) -> None:
    if not lessons:
        # Если список занятий пуст, выводим сообщение "Занятия не найдены."
        print("Занятия не найдены.")
    else:
        for lesson in lessons:
            # Выводим каждое занятие в формате "дата номер_комнаты \"имя_преподавателя\""
            print(f"{lesson.date} {lesson.room} \"{lesson.teacher}\"")

def main():
    lessons = read("in.txt")

    # Запрос параметров у пользователя
    find_teacher = input("Введите имя преподавателя (или оставьте пустым): ")
    find_room = input("Введите номер комнаты (или оставьте пустым): ")
    find_date = input("Введите дату (в формате ГГГГ.ММ.ДД или оставьте пустым): ")

    # Фильтрация занятий
    filtered_lessons = filter_lessons(lessons, find_teacher, find_room, find_date)

    # Вывод отфильтрованных занятий
    show(filtered_lessons)

if __name__ == "__main__":
    main()
