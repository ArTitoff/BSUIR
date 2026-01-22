#pragma once
#include "Student.h"

class Absences {
protected:
    map<int, vector<int>> absences;
public:

    void Print_Absences(Student& student);

    void Initialize_Absences(Student& student);

    void Add_Absence(Student& student);

    void Delete_Absence(Student& student);
};