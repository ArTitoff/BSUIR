#include "Absences.h"

void Absences::Print_Absences(Student& student) {
    if (absences.find(student.Get_ID()) == absences.end()) {
        Initialize_Absences(student);
    }

    cout << "Пропуски студента " << student.Get_Name() << " : " << absences[student.Get_ID()][0] << endl;
}

void Absences::Initialize_Absences(Student& student) {
    absences[student.Get_ID()] = vector<int>(1, 0);
}

void Absences::Add_Absence(Student& student) {
    if (absences.find(student.Get_ID()) == absences.end()) {
        Initialize_Absences(student);
    }
    if (absences.find(student.Get_ID()) != absences.end()) {
        absences[student.Get_ID()][0] += 2;
        Print_Absences(student);
    }
    else {
        cout << "Студент с ID " << student.Get_ID() << " не найден!" << endl;
    }
}

void Absences::Delete_Absence(Student& student) {
    if (absences.find(student.Get_ID()) != absences.end() && absences[student.Get_ID()][0] > 0) {
        absences[student.Get_ID()][0] -= 2;
    }
    else {
        cout << "Студент " << student.Get_Name() << " с ID " << student.Get_ID() << " и так имеет 0 пропусков!" << endl;
    }
}