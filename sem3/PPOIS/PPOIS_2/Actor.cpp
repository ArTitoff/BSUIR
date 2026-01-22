#include "Actor.h"

Actor::Actor(string role, int salary, string hire_date, string job_title, int work_experience, int stress_level, string name, int age)
	: role(role), Workers(salary, hire_date, job_title, work_experience, stress_level, name, age) {}

void Actor::Set_Object_Info() {
	cout << "¬ведите роль актера: ";
	cin >> role;
}

string Actor::Get_Name() const {
	return name;
}

string Actor::Get_Role() const {
	return role;
}