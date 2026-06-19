#pragma once
#include "Workers.h"

class Cleaner : public Workers {
	vector<string> clean_tools;
public:
	Cleaner(vector<string> clean_tools, int salary, string hire_date, string job_title, 
		    int work_experience, int stress_level, string name, int age);

	void Set_Object_Info() override;
};