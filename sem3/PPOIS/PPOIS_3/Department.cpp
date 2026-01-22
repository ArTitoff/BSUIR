#include "Department.h"

Department::Department(const string& name) :
    department_name(name) {}

void Department::Print_Department() const {
    cout << "\nКафедра: " << department_name << endl;
}

string Department::Get_Department_Name() {
    return department_name;
}