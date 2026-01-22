#pragma once
#include "Person.h"

class Event {
protected:
	int duration; //продолжительность
	double rating;
	string genre;
	string show_name;
	int member_amount;
	int rehearsals_count; //количество репетиций
	string premiere_date;
	string description;
	virtual ~Event();
	Event(int duration, double rating, string genre, string show_name, int member_amount, int rehearsals_count,
		string premiere_date, string description);
};