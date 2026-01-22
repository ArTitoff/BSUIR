#pragma once
#include "Workers.h"


class Manager : public Workers {
protected:
	string worker_of_month;

	void Correct_Date(string& hire_date);

	void Check_Age(int& age);

	void Check_Salary(int& salary);

	void Check_Work_Expirience(int& work_experience);

	void Check_Stress_Level(int& stress_level);

	void Check_Hire_Date(string& hire_date);

	void Hire_Employ_Next_Part(Workers* worker);

	void Choosed_Worker_2(const int& choice, Workers* worker1, Workers* worker2, Workers* worker3, Workers* worker4);

	void Choosed_Worker(const int& choice, Workers* worker1, Workers* worker2, Workers* worker3, Workers* worker4);

public:
	void Set_Object_Info() override;

	Manager(string worker_of_month, int salary, string hire_date, string job_title, int work_experience,
		int stress_level, string name, int age);

	void Print() const;



	void Hire_Employ(Workers* worker1, Workers* worker2, Workers* worker3, Workers* worker4);

	void Fire_Employ(Workers* worker1, Workers* worker2, Workers* worker3, Workers* worker4);


};