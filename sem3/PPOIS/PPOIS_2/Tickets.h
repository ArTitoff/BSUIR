#pragma once
#include "Person.h"

class Tickets {
protected:
	int orchestra_tickets_amount;
	int performance_tickets_amount;
	int ticket_orchestra_price;
	int ticket_performance_price;

	Tickets(int orchestra_tickets_amount, int performance_tickets_amount, int ticket_orchestra_price, int ticket_performance_price);
};