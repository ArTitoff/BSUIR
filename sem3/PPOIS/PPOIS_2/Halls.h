#pragma once
#include "Person.h"


class Halls {
protected:
	bool occupied = false;
	int seats_amount;
	int rows; // Количество рядов
	int cols; // Количество мест в ряду
	vector<vector<bool>> hall_map;

public:
	Halls(int cols, int rows);

	void Set_Place_Status(bool status, int& i, int& j);

	bool Get_Place_Status(int& i, int& j);
	int Get_Rows() const;
	int Get_Cols() const;

	void Print_Hall_Map();

	bool Is_Occupied() const;

	int Get_Seats_Amount() const;
};