#include "Student.h"

Student::Student(int ID, string name, int age) :
    ID(ID), Person(name, age) {}

int Student::Get_ID() {
    return ID;
}

void Student::Info() {
    cout << "Имя: " << name << "   ID: " << ID << endl;
}

void Student::Add_Grade(Subject& subject, int grade) {
    grades[subject.Get_Subject_Name()].push_back(grade);
    avarage_sem_grade.push_back(grade);
}

void Student::Delete_Grade(Subject& subject, int grade) {
    auto it = find(grades[subject.Get_Subject_Name()].begin(), grades[subject.Get_Subject_Name()].end(), grade);

    if (it != grades[subject.Get_Subject_Name()].end()) {
        // Запоминаем индекс, чтобы не использовать итератор для другого вектора
        size_t index = distance(grades[subject.Get_Subject_Name()].begin(), it);

        // Удаляем оценку из grades
        grades[subject.Get_Subject_Name()].erase(it);

        // Удаляем соответствующую оценку из avarage_sem_grade
        if (index < avarage_sem_grade.size()) {
            avarage_sem_grade.erase(avarage_sem_grade.begin() + index);
        }

        cout << "Оценка " << grade << " удалена." << endl;
    }
    else {
        cout << "Оценка " << grade << " не найдена." << endl;
    }
}

void Student::Print_Subject_Grades(Subject& subject) {
    if (grades[subject.Get_Subject_Name()].size() > 0) {
        cout << "-------------------------------------------------" << endl;
        cout << subject.Get_Subject_Name() << ": | ";
        double total_grade = 0;
        for (double grade : grades[subject.Get_Subject_Name()]) {
            cout << grade << " | ";
            total_grade += grade;
        }
        double average_grade = total_grade / grades[subject.Get_Subject_Name()].size();
        cout << "   средняя оценка: " << average_grade << endl;
        cout << "-------------------------------------------------" << endl;
    }
    else {
        cout << subject.Get_Subject_Name() << ": " << "Без оценок" << endl;
    }
}


double Student::Print_Avarage_Sem_Grade() {
    double av_sem_gr = 0;
    if (avarage_sem_grade.size() > 0) { // Проверка на пустой вектор
        for (double grade : avarage_sem_grade) {
            av_sem_gr += grade;
        }
        return av_sem_gr / avarage_sem_grade.size();
    }
    else {
        return 0;
    }
}