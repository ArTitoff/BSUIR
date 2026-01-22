#pragma once
#include "Value_Exception.h"
using namespace std;

class Person {
protected:
    string name;
    int age;
    string email;
public:
    ~Person();

    Person(string name, int age);
    virtual void Info() = 0;

    string Get_Name();
};