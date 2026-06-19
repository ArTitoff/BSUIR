#pragma once
#include "Theater.h"

class Handyman : public Workers {
public:
	Handyman(int salary, string hire_date, string job_title, int work_experience, int stress_level, string name, int age);


	void Set_Object_Info() override;

	void Fix_Theater(Theater& theater);
};