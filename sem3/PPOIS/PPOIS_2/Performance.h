#pragma once
#include "Event.h"
#include "Actor.h"

class Performance : public Event {
	vector<string> decorations;
	vector<Actor> actors;
public:
	void Add_Actor(Actor& actor);

	Performance(vector<string> decorations, int duration, double rating, string genre, string show_name, int member_amount,
		int rehearsals_count, string premiere_date, string description);

	string Get_Show_Name() const;

	string Get_Premiere_Date() const;

	void Print_Info() const;
};