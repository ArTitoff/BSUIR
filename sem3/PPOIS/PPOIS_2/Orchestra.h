#pragma once
#include "Event.h"
#include "Musician.h"

class Orchestra : public Event {
	bool conductor; //дирижер
	vector<Musician> musicians;
public:
	Orchestra(bool conductor, int duration, double rating, string genre, string show_name, int member_amount,
		int rehearsals_count, string premiere_date, string description);

	void Add_Musician(Musician& musician);

	string Get_Show_Name() const;

	string Get_Premiere_Date() const;

	void Print_Info() const;

};