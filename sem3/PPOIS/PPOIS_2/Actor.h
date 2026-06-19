#pragma once
#include "Workers.h"

class Actor : public Workers {
protected:
	string role;
public:
	Actor(string role, int salary, string hire_date, string job_title, int work_experience, int stress_level, string name, int age);

	void Set_Object_Info() override;


	string Get_Name() const;

	string Get_Role() const;
};