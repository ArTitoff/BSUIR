#pragma once
#include "Orchestra.h"
#include "Performance.h"

#include "Manager.h"
#include "Tickets.h"
#include "Halls.h"
#include "Author.h"
#include "Visitor.h"
#include "Chashier.h"
#include "Cleaner.h"

class Theater {
	string name = "BSUIR Theater";
	string telephone = "+375 1234";
	string address = "Gikalo 10";
	string site = "bsuirtheater.by";
	bool cool_status = false;
	vector<string> reviews;
	vector<string> vacancies;

	vector<Performance> performances; // Вектор для хранения представлений
	vector<Orchestra> orchestras; // Вектор для хранения оркестров

public:
	void Set_Cool_Status(bool cool_status);
	void Add_Performance(Performance& performance);

	void Add_Orchestra(Orchestra& orchestra);

	void List_of_Events();

	void Check_Index(int& index, int size1, int size2);

	void Show_Event_Info();

	void Choosed_Menu(const int& choice, Manager& worker1, Chashier& worker2, Workers& worker3, Workers& worker4, Workers& worker5);

	void Menu(Manager& worker1, Chashier& worker2, Workers& worker3, Workers& worker4, Workers& worker5);
};