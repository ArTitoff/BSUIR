from __future__ import annotations
from typing import List, Optional
from datetime import date

class Department:
    def __init__(self, name: str, courses: List[Course] = []) -> None:
        self.name = name
        self.courses: List[Course] = courses

    def addCourse(self, course: Course)->None:
        if course not in self.courses:
            self.courses.append(course)


class Grade:
    def __init__(self, value: float, date: date) -> None:
        self.value = value
        self.date = date


    def getValue(self):
        return self.value


class Enrollment:
    def __init__(self, student: Student, course: Course, grade: List[Grade] = []):
        self.grades: List[Grade] = grade
        self.student = student
        self.course = course


    def addGrade(self, value: float)-> None:
        grade = Grade(value, date.today())
        self.grades.append(grade)


    def finalGrade(self)->Grade:
        avg_grade = 0.0

        for grade in self.grades:
            avg_grade += grade.getValue()

        avg_grade = avg_grade / len(self.grades)
        res_grade = Grade(avg_grade, date.today())

        return res_grade
    

    def getStudent(self)->Student:
        return self.student
    

class Course:
    def __init__(self, title: str, teacher: Teacher, department: Department, enrollments: Enrollment = []):
        self.title = title
        self.teacher: Teacher = teacher
        self.enrollments: List[Enrollment] = enrollments
        self.department: Department = department


    def getEnrolledStudents(self)->List[Student]:
        students = []
        for enrollment in self.enrollments:
            students.append(enrollment.getStudent())
        return students
    

    def averageGrade(self)-> float:
        grades: List[Grade] = []
        for enrollment in self.enrollments:
            grades.append(enrollment.finalGrade())

        avg_grade = 0.0

        for grade in grades:
            avg_grade += grade.getValue()
        avg_grade = avg_grade / len(grades)

        return avg_grade


    def add_enrollment(self, enrollment)-> None:
        if enrollment not in self.enrollments:
            self.enrollments.append(enrollment)
     

class Student:
    def __init__(self, name: str) -> None:
        self.name = name
        self.enrollments: List[Enrollment] = []
        self.transcript : Transcript = Transcript()


    def enrollIngCourse(self, course: Course)-> Enrollment:
        enrollment = Enrollment(self, course)

        self.enrollments.append(enrollment)
        self.transcript.enrollments.append(enrollment)
        
        course.add_enrollment(enrollment)
        return enrollment


    def getTranscript(self)-> Transcript:
        return self.transcript


class Transcript:
    def __init__(self, enrollments: List[Enrollment] = []) -> None:
        self.enrollments: List[Enrollment] = enrollments


    def calculateGPA(self)-> float:
        grades: List[Grade] = []
        for enrollment in self.enrollments:
            grades.append(enrollment.finalGrade())

        avg_grade = 0.0

        for grade in grades:
            avg_grade += grade.getValue()
        avg_grade = avg_grade / len(grades)

        return avg_grade


    def print(self)->None:
        avg_grade = self.calculateGPA()
        print(avg_grade)


class Teacher:
    def __init__(self, name: str, courses: List[Course] = []) -> None:
        self.name = name
        self.courses: List[Course] = courses


    def assignToCourse(self, course: Course)-> None:
        if course not in self.courses:
            self.courses.append(course)


    def evaluateStudent(self, enrollment: Enrollment, value: float)->Grade:
        grade = Grade(value, date.today())
        enrollment.addGrade(value)

        return grade
    

    def getName(self)->str:
        return self.name


    def setName(self, name)->None:
        self.name = name



def main():
    department = Department("IIT")
    teacher = Teacher("Nikita Zotov")
    student = Student("Maxim Zinovich")

    course = Course("OMIS", teacher, department)

    enrollment = student.enrollIngCourse(course)

    teacher.assignToCourse(course)
    grade = teacher.evaluateStudent(enrollment, 52)

    transcript = student.getTranscript()

    GPA = transcript.calculateGPA()

    transcript.print()

if __name__ == '__main__':
    main()


