import unittest
from unittest.mock import patch, mock_open
import datetime
from io import StringIO
import sys

from OppO import Lesson, LessonParser, read, filter_lessons, show

# Класс TestLessonParser содержит тесты для методов класса LessonParser
class TestLessonParser(unittest.TestCase):
    def test_extract_date(self):
        self.assertEqual(LessonParser.extract_date("2023.10.01 1-01 \"Иван Иванович\""), datetime.date(2023, 10, 1))
        # Проверяем, что метод выбрасывает исключение при неверном формате даты
        with self.assertRaises(ValueError):
            LessonParser.extract_date("Invalid date format")

    # Тест для метода extract_date с неверным форматом даты
    def test_extract_date_invalid_format(self):
        with self.assertRaises(ValueError):
            LessonParser.extract_date("2025-10-12")

    # Тест для метода extract_room
    def test_extract_room(self):
        self.assertEqual(LessonParser.extract_room("2023.10.01 1-01 \"Иван Иванович\""), "1-01")
        with self.assertRaises(ValueError):
            LessonParser.extract_room("Invalid room format")

    # Тест для метода extract_teacher
    def test_extract_teacher(self):
        self.assertEqual(LessonParser.extract_teacher("2023.10.01 1-01 \"Иван Иванович\""), "Иван Иванович")
        with self.assertRaises(ValueError):
            LessonParser.extract_teacher("Invalid teacher format")

    # Тест для метода extract_room с неверным форматом комнаты
    def test_extract_room_invalid_format(self):
        with self.assertRaises(ValueError):
            LessonParser.extract_room("2023.10.01 101 \"Иван Иванович\"")

# Класс TestLessonFunctions содержит тесты для функций работы с занятиями
class TestLessonFunctions(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="2023.10.01 1-01 \"Иван Иванович\"\n2023.10.02 1-02 \"Петр Петрович\"")
    def test_read(self, mock_file):
        # Проверяем, что функция корректно считывает данные из файла и создает объекты Lesson
        lessons = read("in.txt")
        self.assertEqual(len(lessons), 2)
        self.assertEqual(lessons[0].date, datetime.date(2023, 10, 1))
        self.assertEqual(lessons[0].room, "1-01")
        self.assertEqual(lessons[0].teacher, "Иван Иванович")
        self.assertEqual(lessons[1].date, datetime.date(2023, 10, 2))
        self.assertEqual(lessons[1].room, "1-02")
        self.assertEqual(lessons[1].teacher, "Петр Петрович")

    # Тест для функции filter_lessons
    def test_filter_lessons(self):
        lessons = [
            Lesson(datetime.date(2023, 10, 1), "1-01", "Иван Иванович"),
            Lesson(datetime.date(2023, 10, 2), "1-02", "Петр Петрович"),
            Lesson(datetime.date(2023, 10, 3), "1-03", "Иван Иванович")
        ]
        filtered = filter_lessons(lessons, find_teacher="Иван Иванович")
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].teacher, "Иван Иванович")
        self.assertEqual(filtered[1].teacher, "Иван Иванович")

    # Тест для функции show
    @patch('sys.stdout', new_callable=StringIO)
    def test_show(self, mock_stdout):
        lessons = [
            Lesson(datetime.date(2023, 10, 1), "1-01", "Иван Иванович"),
            Lesson(datetime.date(2023, 10, 2), "1-02", "Петр Петрович")
        ]
        # Проверяем, что функция корректно выводит список занятий на экран
        show(lessons)
        output = mock_stdout.getvalue()
        self.assertIn("2023-10-01 1-01 \"Иван Иванович\"", output)
        self.assertIn("2023-10-02 1-02 \"Петр Петрович\"", output)

    # Негативный тест для функции filter_lessons с неверным форматом данных
    def test_filter_lessons_invalid_format(self):
        lessons = [
            Lesson(datetime.date(2023, 10, 12), "1-01", "Иван Иванович"),
            Lesson(datetime.date(2023, 10, 2), "1-02", "Петр Петрович")
        ]
        with self.assertRaises(ValueError):
            filter_lessons(lessons, find_date="2025-10-12")

# Запуск тестов
if __name__ == "__main__":
    unittest.main()
