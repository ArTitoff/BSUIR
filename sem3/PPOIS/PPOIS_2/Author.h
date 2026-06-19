#pragma once
#include "Workers.h"

class Author : public Workers {
protected:
	vector<string> written_works;
public:
	Author(vector<string> written_works, int salary, string hire_date, string job_title, int work_experience,
		int stress_level, string name, int age);

	void Set_Object_Info() override;

	vector<string> Get_Written_Works();

	void Info();
};