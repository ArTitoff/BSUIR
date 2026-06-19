#include "Authorization.h"

Authorization::Authorization(string login, string password, Student* student, Group* group)
    : login(login), password(password), student(student), group(group), teacher(nullptr) {}

Authorization::Authorization(string login, string password, Teacher* teacher)
    : login(login), password(password), teacher(teacher), student(nullptr), group(nullptr) {}

Student* Authorization::Get_Student() const {
    return student;
}

Group* Authorization::Get_Group_For_Menu() {
    return group;
}

Teacher* Authorization::Get_Teacher() const {
    return teacher;
}

string Authorization::Get_Login() const {
    return login;
}

string Authorization::Get_Password() {
    return password;
}