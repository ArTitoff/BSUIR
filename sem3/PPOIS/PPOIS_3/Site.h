#pragma once
#include "Student.h"
#include "Teacher.h"
#include "Absences.h"
#include "Annoucement.h"
#include "Salary.h"
#include "Department.h"
#include "Group.h"
#include "Starosta.h"
#include "Authorization.h"
#include "Timetable.h"

class Site {
protected:
    static const string site_name;
    static const string telephone;
    vector<Group> groups;
    vector<Department> departments;
    vector<Authorization> authorization;
    vector<Teacher> teachers;
    vector<Subject> subjects;
    Absences absence;
    Timetable timetable;
    vector<Announcement> annoucements;
    Salary salary;
public:

    void Add_Stud_Authorization(string& login, string& password, Student* student, Group* group);

    void Add_Teacher_Authorization(string& login, string& password, Teacher* teacher);

    void Remove_Student_Authorization(Student* student);

    void Remove_Teacher_Authorization(Teacher* teacher);

    void Add_Announcement();

    void Delete_Announcement();

    void Timetable_Of_Group(Group& group);

    void Print_Site_Info();


    void Add_Department(Department& department);

    void Add_Department();
    void Delete_Department();


    void Add_Department(const string& name);

    void Add_Subject();

    void Delete_Subject();

    void Add_Subject(Subject& subject);

    void Add_Teacher(Teacher& teacher);

    void Delete_Teacher();

    void Add_Teacher();

    void Add_Student();

    void Delete_Student();

    void Add_Group();

    void Delete_Group();

    void Add_Group(Group& group);

    void Add_Pre_Stud_To_Group(Group& group, Student& stud);

    void Teacher_Menu(Teacher& teacher);

    void Get_Group_Num(int& choice);

    void Choosed_Menu_Teacher(const int& choice, Teacher& teacher);

    void Student_Menu(Student& student, Group& group);

    void Choosed_Menu_Student(const int& choice, Student& student, Group& group);

    void Admin_Menu();

    void Choosed_Menu_Admin(const int& choice);

    void Main_Menu();

    void Choosed_Main_Menu(const int& choice);
};