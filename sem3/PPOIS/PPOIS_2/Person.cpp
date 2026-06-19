#include "Person.h"
Person::Person(string name, int age) :
	name(name), age(age) {}

void Person::Info() {
	cout << "Name: " << name << ", Age: " << age << endl;
}

Person:: ~Person() {
}

string Person::Get_Name() {
	return name;
}