#include "Workers.h"

Workers::Workers(int salary, string hire_date, string job_title, int work_experience, int stress_level, string name, int age)
	: salary(salary), hire_date(hire_date), job_title(job_title), work_experience(work_experience), stress_level(stress_level), Person(name, age) {
	hired = true;
}

Workers::~Workers() {
}

   void Workers::Info() {
	Person::Info(); // Вызов метода info() из базового класса
	cout << "Salary: " << salary << ",\tHire Date: " << hire_date
		<< ",\tJob Title: " << job_title << ",  Work Experience : " << work_experience
		<< ",  Stress Level: " << stress_level << endl;
}

   void Workers::Set_Name(string& name) {
	   this->name = name;
   }

   void Workers::Set_Age(int& age) {
	   this->age = age;
   }

   void Workers::Set_Salary(int& salary) {
	   this->salary = salary;
   }

   void Workers::Set_Hire_Date(string& hire_date) {
	   this->hire_date = hire_date;
   }

   void Workers::Set_Job_Title(string& job_title) {
	   this->job_title = job_title;
   }

   void Workers::Set_Work_Experience(int& work_experience) {
	   this->work_experience = work_experience;
   }

   void Workers::Set_Stress_Level(int& stress_level) {
	   this->stress_level = stress_level;
   }

   void Workers::Set_Hired_Status(bool hired) {
	   this->hired = hired;
   }

   bool Workers::Get_Hired_Status() const {
	   return hired;
   }