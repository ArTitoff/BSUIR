#include "Author.h"

Author::Author(vector<string> written_works, int salary, string hire_date, string job_title, int work_experience,
	int stress_level, string name, int age)
	: written_works(written_works), Workers(salary, hire_date, job_title, work_experience, stress_level, name, age) {}

void Author::Set_Object_Info() {
	written_works.clear();
	int list_size;

	while (true) {
		cout << "Введите число списка работ: ";
		cin >> list_size;

		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}

		try {
			if (list_size < 0) throw Value_Exception("Некорректное число списка работ: " + to_string(list_size));
			break;
		}
		catch (const Value_Exception& e) {
			cout << "Ошибка: " << e.what() << endl;
		}
	}

	cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Очистка буфера после ввода числа

	for (int i = 0; i < list_size; i++) {
		cout << "Введите работу №" << i + 1 << ": ";
		string work;
		getline(cin, work);
		written_works.push_back(work);
	}
	cout << "\nДанные записаны: \n";

}

void Author::Info() {
	Workers::Info(); // Вызов метода displayInfo() из класса Workers
	cout << "Written Works: ";
	for (const string& work : written_works) {
		cout << work << "; ";
	}
	cout << endl;
}

vector<string>  Author::Get_Written_Works() {
	return written_works;
}