class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def get_avg_grade(self):
        if not self.grades:
            return 0
        total = sum(sum(grades) for grades in self.grades.values())
        count = sum(len(grades) for grades in self.grades.values())
        return total / count

    def __str__(self):
        avg_grade = self.get_avg_grade()
        courses_in_progress = ', '.join(self.courses_in_progress) if self.courses_in_progress else 'Нет курсов'
        finished_courses = ', '.join(self.finished_courses) if self.finished_courses else 'Нет курсов'
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg_grade:.1f}\n"
                f"Курсы в процессе изучения: {courses_in_progress}\n"
                f"Завершенные курсы: {finished_courses}")

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_avg_grade() < other.get_avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_avg_grade() == other.get_avg_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def get_avg_grade(self):
        if not self.grades:
            return 0
        total = sum(sum(grades) for grades in self.grades.values())
        count = sum(len(grades) for grades in self.grades.values())
        return total / count

    def __str__(self):
        avg_grade = self.get_avg_grade()
        return f"{super().__str__()}\nСредняя оценка за лекции: {avg_grade:.1f}"

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_avg_grade() < other.get_avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_avg_grade() == other.get_avg_grade()

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        super().rate_hw(student, course, grade)

    def __str__(self):
        return f"{super().__str__()}Проверяющий"

