#include "Visitor.h"

Visitor::Visitor(string visit_aim, int money, string name, int age)
	  : visit_aim(visit_aim), money(money), Person(name, age) {}

int Visitor::Get_Money() const {
	return money;
}