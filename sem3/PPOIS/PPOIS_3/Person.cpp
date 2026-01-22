#include "Person.h"

Person::~Person() {}

Person::Person(string name, int age) :
    name(name), age(age) {}

string Person::Get_Name() {
    return name;
}
