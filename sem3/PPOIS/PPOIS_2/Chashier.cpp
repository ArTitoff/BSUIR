#include "Chashier.h"

void Chashier::Check_Choice(int& choice) {
	while (true) {
		cout << "\nВведите 1, чтобы забронировать место:\nВведите 2, чтобы убрать бронирование: ";
		cin >> choice;

		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}

		try {
			if (choice < 1 || choice > 2) throw Value_Exception("Некорректный выбор");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}
}

void Chashier::Check_Choice_2(int& choice) {
	while (true) {
		cout << "\n\nВведите 1, чтобы забронировать место в Оркестре:\nВведите 2, чтобы забронировать место в Театре: ";
		cin >> choice;

		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}

		try {
			if (choice < 1 || choice > 2) throw Value_Exception("Некорректный выбор");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}
}

void Chashier::Book_Orch() {
	int choice1, choice2;
	while (true) {
		cout << "Введите номер ряда: ";
		cin >> choice1;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (choice1 < 1 || choice1 > orchestra_hall.Get_Rows()) throw Value_Exception("Такого ряда нет");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}

	while (true) {
		cout << "Введите номер места: ";
		cin >> choice2;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (choice2 < 1 || choice2 > orchestra_hall.Get_Cols()) throw Value_Exception("Такого места нет");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}
	choice1 = choice1 - 1;
	choice2 = choice2 - 1;

	if (orchestra_hall.Get_Place_Status(choice1, choice2)) {
		cout << "\nЭто место уже занято\n";
		void Book_Orch();
	}
	else {
		cout << "\nМесто успешно забронировано\n";
		orchestra_hall.Set_Place_Status(true, choice1, choice2);
		tickets_profit += ticket_orchestra_price; //добавляем в общую кассу
		orchestra_tickets_amount--;
	}

}

void Chashier::Book_Perf() {
	int choice1, choice2;
	while (true) {
		cout << "Введите номер ряда: ";
		cin >> choice1;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (choice1 < 1 || choice1 > theater_hall.Get_Rows()) throw Value_Exception("Такого ряда нет");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}

	while (true) {
		cout << "Введите номер места: ";
		cin >> choice2;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (choice2 < 1 || choice2 > theater_hall.Get_Cols()) throw Value_Exception("Такого места нет");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}
	choice1 = choice1 - 1;
	choice2 = choice2 - 1;
	if (theater_hall.Get_Place_Status(choice1, choice2)) {
		cout << "\nЭто место уже занято\n";
		Book_Perf();
	}
	else {
		cout << "\nМесто успешно забронировано\n";
		theater_hall.Set_Place_Status(true, choice1, choice2);
		tickets_profit += ticket_performance_price; //добавляем в общую кассу
		performance_tickets_amount--;
	}
}

void Chashier::UnBook_Orch() {
	int choice1, choice2;
	while (true) {
		cout << "Введите номер ряда: ";
		cin >> choice1;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (choice1 < 1 || choice1 > orchestra_hall.Get_Rows()) throw Value_Exception("Такого ряда нет");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}

	while (true) {
		cout << "Введите номер места: ";
		cin >> choice2;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (choice2 < 1 || choice2 > orchestra_hall.Get_Cols()) throw Value_Exception("Такого места нет");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}
	choice1 = choice1 - 1;
	choice2 = choice2 - 1;
	if (!orchestra_hall.Get_Place_Status(choice1, choice2)) {
		cout << "\nЭто место итак не забронированно\n";
		 Book_Orch();
	}
	else {
		cout << "\nМесто успешно разбронировано\n";
		orchestra_hall.Set_Place_Status(false, choice1, choice2);
		tickets_profit -= ticket_orchestra_price; // убираем из общей кассы
		orchestra_tickets_amount++;
	}

}

void Chashier::UnBook_Perf() {
	int choice1, choice2;
	while (true) {
		cout << "Введите номер ряда: ";
		cin >> choice1;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (choice1 < 1 || choice1 > theater_hall.Get_Rows()) throw Value_Exception("Такого ряда нет");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}

	while (true) {
		cout << "Введите номер места: ";
		cin >> choice2;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (choice2 < 1 || choice2 > theater_hall.Get_Cols()) throw Value_Exception("Такого места нет");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}
	choice1 = choice1 - 1;
	choice2 = choice2 - 1;

	if (!theater_hall.Get_Place_Status(choice1, choice2)) {
		cout << "\nЭто место итак не забронированно\n";
		Book_Perf();
	}
	else {
		cout << "\nМесто успешно разбронировано\n";
		theater_hall.Set_Place_Status(false, choice1, choice2);
		tickets_profit -= ticket_performance_price; // убираем из общей кассы
		performance_tickets_amount++;
	}
}

void Chashier::Book_For_Visitor(Visitor& visitor, int rows, int cols, int choice) {
	rows--;
	cols--;

	if (visitor.Get_Money() > ticket_orchestra_price && choice == 1 && orchestra_tickets_amount != 0) {
		if (orchestra_hall.Get_Rows() < rows + 1 || 0 > rows + 1 || orchestra_hall.Get_Cols() < cols + 1 || 0 > cols + 1) return;
		if (orchestra_hall.Get_Place_Status(rows, cols)) {
			cout << "Место занято\n";
			return;
		}

		orchestra_hall.Set_Place_Status(true, rows, cols);
		cout << "Пользователь " << visitor.Get_Name() << " успешно забронировал место " << rows + 1 << ',' << cols + 1 << " в зале Оркестра\n";

		tickets_profit += ticket_orchestra_price;
		orchestra_tickets_amount--;
	}
	else if (visitor.Get_Money() > ticket_performance_price && choice == 2 && performance_tickets_amount != 0) {
		if (theater_hall.Get_Rows() < rows + 1 || 0 > rows + 1 || theater_hall.Get_Cols() < cols + 1 || 0 > cols + 1) return;
		if (theater_hall.Get_Place_Status(rows, cols)) {
			cout << "Место занято\n";
			return;
		}

		theater_hall.Set_Place_Status(true, rows, cols);
		cout << "Пользователь " << visitor.Get_Name() << " успешно забронировал место " << rows + 1 << ',' << cols + 1 << " в зале Театра\n";

		tickets_profit += ticket_performance_price;
		performance_tickets_amount--;
	}
	else cout << "Не хватает денег\n";
}

Chashier::Chashier(int salary, string hire_date, string job_title, int work_experience, int stress_level, string name, int age,
	int rows1, int cols1, int rows2, int cols2, int ticket_orch_price, int ticket_per_price)
	: Workers(salary, hire_date, job_title, work_experience, stress_level, name, age),
	theater_hall(rows1, cols1), orchestra_hall(rows2, cols2), Tickets(rows2* cols2, rows1* cols1, ticket_orch_price, ticket_per_price) {}

void Chashier::Set_Object_Info() {
	tickets_profit = 0;
}

void Chashier::Book_Place() {
	int choice;
	Check_Choice(choice);
	if (choice == 1) {
		Check_Choice_2(choice);
		if (choice == 1) {
			orchestra_hall.Print_Hall_Map();
			Book_Orch();
		}
		else {
			theater_hall.Print_Hall_Map();
			Book_Perf();
		}
	}
	else {
		Check_Choice_2(choice);
		if (choice == 1) {
			orchestra_hall.Print_Hall_Map();
			UnBook_Orch();
		}
		else {
			theater_hall.Print_Hall_Map();
			UnBook_Perf();
		}
	}
}