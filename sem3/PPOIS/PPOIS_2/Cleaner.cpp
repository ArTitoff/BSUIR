#include "Cleaner.h"

Cleaner::Cleaner(vector<string> clean_tools, int salary, string hire_date, string job_title, int work_experience, int stress_level, string name, int age)
	: clean_tools(clean_tools), Workers(salary, hire_date, job_title, work_experience, stress_level, name, age) {}

void Cleaner::Set_Object_Info() {
	clean_tools.clear();
	int list_size;

	while (true) {
		cout << "Введите число списка инструментов: ";
		cin >> list_size;

		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}

		try {
			if (list_size < 0) throw Value_Exception("Некорректное число списка инструментов: " + to_string(list_size));
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
		clean_tools.push_back(work);
	}
	cout << "\nДанные записаны: \n";

}