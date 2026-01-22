#include "Header.h"
#include <iostream>

using namespace std;

/**
	@brief Function for creating random Field
*/

void Piatnashky::CerateRandomField() {
	srand(time(NULL));
	bool Random[16];
	for (int i = 0; i < 16;i++)
		Random[i] = false;

	for (int j = 0; j < 4;j++) {
		for (int k = 0; k < 4;k++) {
			int RNum = rand() % 16;
			if (!Random[RNum]) {
				this->Field[j][k] = RNum;
				Random[RNum] = true;
				if (RNum == 0) {
					PointX = j;
					PointY = k;
				}
			}
			else k--;
		}
	}
	Print();
}

/** @brief Function for output game board
*/
void Piatnashky::Print() {
	cout << "---------------------------\n";
	for (int i = 0; i < 4;i++) {
		for (int j = 0; j < 4;j++)
			if (Field[i][j] == 0) {
				cout << "X\t";
			}
			else cout << Field[i][j] << "\t";
		cout << endl;
	}
	cout << "---------------------------\n\n";
}

/** @brief Function for switch left
*/

void Piatnashky::SwapLeft() {
	if (PointY > 0) {
		Field[PointX][PointY] = Field[PointX][PointY - 1];
		Field[PointX][PointY - 1] = 0;
		PointY--;
	}
	else cout << "Нельзя передвинуть\n\n";
	Print();
}

/** @brief Function for switch right
*/
void Piatnashky::SwapRight() {
	if (PointY < 3) {
		Field[PointX][PointY] = Field[PointX][PointY + 1];
		Field[PointX][PointY + 1] = 0;
		PointY++;
	}
	else cout << "Нельзя передвинуть\n\n";
	Print();
}

/** @brief Function for switch up
*/
void Piatnashky::SwapUp() {
	if (PointX > 0) {
		Field[PointX][PointY] = Field[PointX - 1][PointY];
		Field[PointX - 1][PointY] = 0;
		PointX--;
	}
	else cout << "Нельзя передвинуть\n\n";
	Print();
}

/** @brief Function for switch down
*/
void Piatnashky::SwapDown() {
	if (PointX < 3) {
		Field[PointX][PointY] = Field[PointX + 1][PointY];
		Field[PointX + 1][PointY] = 0;
		PointX++;
	}
	else cout << "Нельзя передвинуть\n\n";
	Print();
}
/** @brief Function to check if the user has completed the game
*/
/// @param choice If the game is completed, you need to start a new one or end the program
void Piatnashky::Proverka(int& choice) {
	int RCount = 1;
	for (int i = 0; i < 4;i++) {
		for (int j = 0; j < 4;j++) {
			if (Field[i][j] == RCount)
				RCount++;
			else break;
		}
	}
	if (RCount == 16) {
		cout << "\nВы прошли игру!!!\n\n";
		do {
			cout << "Начните новую - 1 или Завершите программу - 0\n";
			cin >> choice;
		} while ((choice != 1) && (choice != 0));
		Menu_2(choice);
	}
}

/** @brief Menu for interaction
*/
void Piatnashky::Menu() {
	int choice;
	do {
		cout << "Меню:" << endl;
		cout << "1. Новая игра" << endl;
		cout << "2. Переместить Х влево" << endl;
		cout << "3. Переместить Х вправо" << endl;
		cout << "4. Переместить Х вверх" << endl;
		cout << "5. Переместить Х вниз" << endl;
		cout << "0. Выйти из игры" << endl;
		cout << "Введите номер команды: ";
		cin >> choice;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(32767, '\n');
			cout << "NECOOR VVOD";
			return;
		}
		cout << endl;
		Menu_2(choice);
		Proverka(choice);
	} while (choice != 0);
}

void Piatnashky::Menu_2(const int& choice) {
	switch (choice) {
	case 1:
		cout << "\nНовая игра началась!" << endl;
		CerateRandomField();
		break;
	case 2:
		SwapLeft();
		break;
	case 3:
		SwapRight();
		break;
	case 4:
		SwapUp();
		break;
	case 5:
		SwapDown();
		break;
	case 0:
		cout << "Программа завершена!" << endl;
		break;
	default:
		cout << "Такого варианта нет" << endl;
	}
}

void Piatnashky::Play() {
	CerateRandomField();
	Menu();

}

/** @brief Class operator to display the value of one cell
*/

/// @param Index of cell you want to see
/// @return Value of cell you select
	int& Piatnashky::operator[](const int& index) {
		int row = index / 4;
		int col = index % 4;
		Print();
		return Field[row][col];

	}

	/** @brief constructor
	*/
	Piatnashky::Piatnashky() {
	 int E = 1;
		for (int j = 0; j < 4;j++) {
			for (int k = 0; k < 4;k++) {
				if (E == 15)
					break;
				else {
					Field[j][k] = E;
					E++;
				}
			}
		}
		Field[3][2] = 0;
		Field[3][3] = 15;
		PointX = 3;
		PointY = 2;
	}
	