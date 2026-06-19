#pragma once
#include "Person.h"
#include "Subject.h"

class Student : public Person {
protected:
    int ID;
    vector<int> avarage_sem_grade;
    map<string, vector<int>> grades;
public:
    Student(int ID, string name, int age);

    int Get_ID();

    void Info() override;

    void Add_Grade(Subject& subject, int grade);

    void Delete_Grade(Subject& subject, int grade);

    void Print_Subject_Grades(Subject& subject);


    double Print_Avarage_Sem_Grade();

};