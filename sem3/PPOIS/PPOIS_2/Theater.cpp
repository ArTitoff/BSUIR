#include "Theater.h"

void Theater::Set_Cool_Status(bool cool_status) {
	this->cool_status = cool_status;
}
void Theater::Add_Performance(Performance& performance) {
	performances.push_back(performance); // Добавление представления
}

void Theater::Add_Orchestra(Orchestra& orchestra) {
	orchestras.push_back(orchestra); // Добавление оркестра
}

void Theater::List_of_Events() {
	cout << "Список представлений и оркестров:\n";

	for (int i = 0; i < performances.size(); i++) {
		cout << i + 1 << ". Представление: " << performances[i].Get_Show_Name()
			<< " - Дата премьеры: " << performances[i].Get_Premiere_Date() << endl;
	}

	for (int i = 0; i < orchestras.size(); i++) {
		cout << performances.size() + i + 1 << ". Оркестр: " << orchestras[i].Get_Show_Name()
			<< " - Дата премьеры: " << orchestras[i].Get_Premiere_Date() << endl;
	}
}

void Theater::Check_Index(int& index, int size1, int size2) {
	while (true) {
		cout << "\nВведите номер события, о котором хотите узнать полную информацию: ";
		cin >> index;

		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}

		try {
			if (index < 1 || index > size1 + size2) throw Value_Exception("Некорректный выбор");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}
	index = index - 1;
}

void Theater::Show_Event_Info() {
	int index;
	if (performances.size() + orchestras.size() < 1) {
		cout << "Представлений нет!\n\n";
		return;
	}
	Check_Index(index, performances.size(), orchestras.size());
	if (index < performances.size())
		performances[index].Print_Info(); // Вывод информации о представлении
	else {
		int a = index - performances.size();
		orchestras[a].Print_Info(); // Вывод информации о оркестре
	}
}

void Theater::Choosed_Menu(const int& choice, Manager& worker1, Chashier& worker2, Workers& worker3, Workers& worker4, Workers& worker5) {
	switch (choice) {
	case 1:
		worker1.Hire_Employ(&worker2, &worker3, &worker4, &worker5);
		break;
	case 2:
		worker1.Fire_Employ(&worker2, &worker3, &worker4, &worker5);
		break;
	case 3:
		worker2.Book_Place();
		break;
	case 4:
		List_of_Events();
		break;
	case 5:
		List_of_Events();
		Show_Event_Info();
		break;
	case 6:
		cout << "Хорошего дня!\n";
		break;
	default:
		cout << "Такого варианта нет" << endl;
	}
}

void Theater::Menu(Manager& worker1, Chashier& worker2, Workers& worker3, Workers& worker4, Workers& worker5) {
	int choice;
	do {
		cout << "1. Нанять работника" << endl;
		cout << "2. Уволить работника" << endl;
		cout << "3. Забронировать место/Отменить бронирование" << endl;
		cout << "4. Афиша" << endl;
		cout << "5. Афиша с просмотром подробной информации конкретного события" << endl;
		cout << "6. Выход" << endl;
		while (true) {
			cout << "Введите номер пункта: ";
			cin >> choice;
			if (cin.fail()) {
				cin.clear();
				cin.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
				continue;
			}
			try {
				if (choice < 0 || choice > 6) throw Value_Exception("Некорректный выбор ");
				break;
			}
			catch (const Value_Exception& e) {
				cout << e.what() << endl;
			}
		}
		cout << endl;
		Choosed_Menu(choice, worker1, worker2, worker3, worker4, worker5);
		cout << endl;
	} while (choice != 6);
}