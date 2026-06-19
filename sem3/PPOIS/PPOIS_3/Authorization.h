#pragma once
#include "Student.h"
#include "Teacher.h"
#include "Group.h"

class Authorization {
protected:
    string login;
    string password;
    Student* student;
    Group* group;
    Teacher* teacher;
public:
    Authorization(string login, string password, Student* student, Group* group);

    Authorization(string login, string password, Teacher* teacher);

    Student* Get_Student() const;
    ;
    Group* Get_Group_For_Menu();

    Teacher* Get_Teacher() const;

    string Get_Login() const;

    string Get_Password();
};