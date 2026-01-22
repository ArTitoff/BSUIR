#include "Musician.h"

Musician::Musician(string playing_instrument, int salary, string hire_date, string job_title, int work_experience,
	int stress_level, string name, int age)
	: playing_instrument(playing_instrument), Workers(salary, hire_date, job_title, work_experience, stress_level, name, age) {}


void Musician::Set_Object_Info() {
	cout << "¬ведите роль актера: ";
	cin >> playing_instrument;
}

string Musician::Get_Name() const {
	return name;
}

string Musician::Get_Playing_Insrument() const {
	return playing_instrument;
}