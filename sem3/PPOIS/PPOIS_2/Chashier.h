#pragma once
#include "Workers.h"
#include "Halls.h"
#include "Tickets.h"
#include "Visitor.h"

class Chashier : public Workers, public Tickets {
protected:
	Halls theater_hall;
	Halls orchestra_hall;
	int tickets_profit = 0;

	void Check_Choice(int& choice);

	void Check_Choice_2(int& choice);

	void Book_Orch();
	void Book_Perf();

	void UnBook_Orch();
	void UnBook_Perf();
public:
	void Book_For_Visitor(Visitor& visitor, int rows, int cols, int choice);

	Chashier(int salary, string hire_date, string job_title, int work_experience, int stress_level, string name, int age,
		int rows1, int cols1, int rows2, int cols2, int ticket_orch_price, int ticket_per_price);
	void Set_Object_Info() override;

	void Book_Place();
};