#include "Halls.h"


Halls::Halls(int cols, int rows) : cols(cols), rows(rows), seats_amount(rows* cols), hall_map(rows, vector<bool>(cols, false)) {
	// Здесь инициализируем hall_map false
}

void Halls::Set_Place_Status(bool status, int& i, int& j) {
	hall_map[i][j] = status;
}

bool Halls::Get_Place_Status(int& i, int& j) {
	return hall_map[i][j];
}
int Halls::Get_Rows() const {
	return rows;
}
int Halls::Get_Cols() const {
	return cols;
}

void Halls::Print_Hall_Map() {
	cout << "   ";
	for (int i = 0; i < cols; i++) {
		cout << " " << i + 1;
	}


	cout << " Место" << endl << endl;
	for (int i = 0; i < rows; i++) {
		cout << i + 1 << "   ";
		for (int j = 0; j < cols; j++) {
			if (hall_map[i][j] == true)
				cout << "X "; // Занятое место
			else cout << "0 "; // Незанятое место
		}
		cout << endl;
	}
	cout << "Ряд\n\n";
}

bool Halls::Is_Occupied() const {
	return occupied;
}

int Halls::Get_Seats_Amount() const {
	return seats_amount;
}