#pragma once
#include "Student.h"
#include "Department.h"

class Group {
protected:
    int group_id;
    int course;
    string speciality;
    Department* department; // Указатель на объект Department
    vector<Student> students;
    vector<Subject> subjects;
    void Sort_Student();
public:
    int Get_Group_ID();
    Group(int id, Department* dept, int course, string speciality);

    void Print_Department();


    int Get_Group_Size();

    void Display();

    void Display_Student_Rating(Student& student);

    vector<Subject> Get_Subjects();

    Student& Get_Student(int i);

    Student* Get_Student_Ptr(int index);

    void Add_Student_To_Group(Student& student);

    void Add_Student_To_Group(int ID, const string& name, int age);
    void Delete_Student_From_Group(int index);


    void Add_Subject_To_Group(Subject& subject);

};