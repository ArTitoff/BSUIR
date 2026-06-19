#pragma once
#include "Person.h"

class Workers : public Person {
protected:
	int salary;
	string hire_date;
	string job_title;
	int work_experience;
	int stress_level;
	bool hired;

public:
	Workers(int salary, string hire_date, string job_title, int work_experience, int stress_level, string name, int age);

	virtual ~Workers();
	virtual void Info() override;

	virtual void Set_Object_Info() = 0;

	void Set_Name(string& name);

	void Set_Age(int& age);

	void Set_Salary(int& salary);

	void Set_Hire_Date(string& hire_date);

	void Set_Job_Title(string& job_title);

	void Set_Work_Experience(int& work_experience);

	void Set_Stress_Level(int& stress_level); 

	void Set_Hired_Status(bool hired);

	bool Get_Hired_Status() const;
};