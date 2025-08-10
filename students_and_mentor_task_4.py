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
        return f"{super().__str__()}\nПроверяющий"


def get_students_course_avg(students, course):
    total = 0
    count = 0
    for student in students:
        if course in student.grades:
            total += sum(student.grades[course])
            count += len(student.grades[course])
    return total / count if count > 0 else 0

def get_lecturers_course_avg(lecturers, course):
    total = 0
    count = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total += sum(lecturer.grades[course])
            count += len(lecturer.grades[course])
    return total / count if count > 0 else 0


student1 = Student('Ruoy', 'Eman', 'male')
student1.courses_in_progress = ['Python', 'Git']
student1.finished_courses = ['Введение в программирование']

student2 = Student('Anna', 'Smith', 'female')
student2.courses_in_progress = ['Python', 'JavaScript']
student2.finished_courses = ['Основы программирования']

lecturer1 = Lecturer('Some', 'Buddy')
lecturer1.courses_attached = ['Python', 'Git']

lecturer2 = Lecturer('Jane', 'Doe')
lecturer2.courses_attached = ['Python', 'JavaScript']

reviewer1 = Reviewer('John', 'Doe')
reviewer1.courses_attached = ['Python', 'Git']

reviewer2 = Reviewer('Alice', 'Cooper')
reviewer2.courses_attached = ['Python', 'JavaScript']

student1.rate_lecture(lecturer1, 'Python', 9)
student1.rate_lecture(lecturer1, 'Git', 8)
student2.rate_lecture(lecturer2, 'Python', 10)
student2.rate_lecture(lecturer2, 'JavaScript', 9)

reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Git', 8)
reviewer2.rate_hw(student2, 'Python', 9)
reviewer2.rate_hw(student2, 'JavaScript', 10)


print()
print("Информация о проверяющих:")
print(reviewer1)
print()
print(reviewer2)

print()
print("Информация о лекторах:")
print(lecturer1)
print()
print(lecturer2)

print()
print("Информация о студентах:")
print(student1)
print()
print(student2)

print()
print("Сравнение лекторов:")
print(f"{lecturer1.name} {lecturer1.surname} > {lecturer2.name} {lecturer2.surname}: {lecturer1 > lecturer2}")

print("\nСравнение студентов:")
print(f"{student1.name} {student1.surname} == {student2.name} {student2.surname}: {student1 == student2}")

print()
course_name = 'Python'
students_avg = get_students_course_avg([student1, student2], course_name)
lecturers_avg = get_lecturers_course_avg([lecturer1, lecturer2], course_name)

print(f"Средняя оценка студентов по курсу {course_name}: {students_avg:.1f}")
print(f"Средняя оценка лекторов по курсу {course_name}: {lecturers_avg:.1f}")