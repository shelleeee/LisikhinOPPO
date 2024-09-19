import re
import datetime

class Lesson:
    def __init__(self, date: datetime.date, room: str, teacher: str) -> None:
        self.date: datetime.date = date
        self.room: str = room
        self.teacher: str = teacher

def extract_date(line: str) -> datetime.date:
    date_str = re.findall(r"\d{4}\.\d{2}\.\d{2}", line)[0]
    return datetime.datetime.strptime(date_str, "%Y.%m.%d").date()

def extract_room(line: str) -> str:
    return re.findall(r"\d-\d{2}", line)[0]

def extract_teacher(line: str) -> str:
    return re.findall(r'"(.+?)"', line)[0]

def read(txt_file: str) -> list:
    result = []
    with open(txt_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            date = extract_date(line)
            room = extract_room(line)
            teacher = extract_teacher(line)
            new_lesson = Lesson(date, room, teacher)
            result.append(new_lesson)
    return result

def show(lessons: list) -> None:
    for lesson in lessons:
        print(f"{lesson.date} {lesson.room} \"{lesson.teacher}\"")

# Пример использования
lessons = read("in.txt")
show(lessons)
