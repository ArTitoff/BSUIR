#include "Handyman.h"

Handyman::Handyman(int salary, string hire_date, string job_title, int work_experience, int stress_level, string name, int age)
	: Workers(salary, hire_date, job_title, work_experience, stress_level, name, age) {}

void Handyman::Set_Object_Info() {
	cout << "Working...\n";
}

void Handyman::Fix_Theater(Theater& theater) {
	Set_Object_Info();
	theater.Set_Cool_Status(true);
	cout << "Вся работа по театру выполнена\n";
}