#pragma once
#include <iostream>
#include <string>
using namespace std;

class Department {

protected:
    string department_name;

public:
    Department(const string& name);

    void Print_Department() const;

    string Get_Department_Name();
};