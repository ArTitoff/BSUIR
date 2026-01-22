#pragma once
#include "Workers.h"

class Musician : public Workers {
protected:
	string playing_instrument;
public:
	Musician(string playing_instrument, int salary, string hire_date, string job_title, int work_experience,
		int stress_level, string name, int age);

	void Set_Object_Info() override;

	string Get_Name() const;

	string Get_Playing_Insrument() const;

};