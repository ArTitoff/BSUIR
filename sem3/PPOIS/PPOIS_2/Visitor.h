#pragma once
#include "Person.h"

class Visitor : public Person {
protected:
	string visit_aim;
	int money;
public:
	Visitor(string visit_aim, int money, string name, int age);

	int Get_Money() const;
};

