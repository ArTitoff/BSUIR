#include "Manager.h"

void  Manager::Correct_Date(string& hire_date) {
	if (hire_date.size() != 10 || hire_date[2] != '.' || hire_date[5] != '.')
		throw Data_Exception("Некорректный ввод даты. Ожидалось: DD.MM.YYYY");

	int date, month, year;
	char dot1, dot2;
	stringstream ss(hire_date);
	ss >> date >> dot1 >> month >> dot2 >> year;

	if (ss.fail() || dot1 != '.' || dot2 != '.' || ss.peek() != EOF)
		throw Data_Exception("Некорректный ввод. Убедитесь, что введены только цифры.");


	if (month < 1 || month > 12)
		throw Data_Exception("Некорректный месяц: " + to_string(month));

	if (date < 1 || date > 31)
		throw Data_Exception("Некорректный день: " + to_string(date));

	if ((month == 4 || month == 6 || month == 9 || month == 11) && date > 30)
		throw Data_Exception("В этом месяце только 30 дней.");

	if (year < 1950 || year > 2100)
		throw Data_Exception("Некорректный ввод года");

	if (month == 2) {
		if (year % 4 == 0 && date > 29) {
			throw Data_Exception("Високосный год, февраль имеет только 29 дней.");
		}
		else if (year % 4 != 0 && date > 28) {
			throw Data_Exception("Февраль имеет только 28 дней в невисокосный год.");
		}
	}
}

void  Manager::Check_Age(int& age) {
	while (true) {
		cout << "Введите возраст: ";
		cin >> age;

		// Проверка на некорректный ввод
		if (cin.fail()) {
			cin.clear(); // Сброс состояния потока
			cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Очистка буфера
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue; // Возврат к началу цикла
		}

		try {
			if (age < 0 || age > 70) throw Value_Exception("Некорректный возраст");
			break; // Если возраст корректен, выходим из цикла
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl; // Вывод сообщения об ошибке
		}
	}
}

void Manager::Check_Salary(int& salary) {
	while (true) {
		cout << "Введите зарплату: ";
		cin >> salary;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (salary < 0) throw Value_Exception("Некорректная зарплата: " + to_string(salary));
			break;
		}
		catch (const Value_Exception& e) {
			cout << "Ошибка: " << e.what() << endl;
		}
	}
}

void Manager::Check_Work_Expirience(int& work_experience) {
	while (true) {
		cout << "Введите опыт работы: ";
		cin >> work_experience;
		if (cin.fail()) {
			//cin.clear();
			//cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			break;
		}
		try {
			if (work_experience < 0) throw Value_Exception("Некорректный опыт работы: " + to_string(work_experience));
			break;
		}
		catch (const Value_Exception& e)
		{
			cout << "Ошибка: " << e.what() << endl;
		}
	}
}

void Manager::Check_Stress_Level(int& stress_level) {
	while (true) {
		cout << "Введите уровень стресса (0-10): ";
		cin >> stress_level;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (stress_level < 0 || stress_level > 10) {
				throw Value_Exception("Некорректный уровень стресса: " + to_string(stress_level));
			}
			break;
		}
		catch (const Value_Exception& e) {
			cout << "Ошибка: " << e.what() << endl;
		}
	}
}

void Manager::Check_Hire_Date(string& hire_date) {
	while (true) {
		cout << "Введите дату найма (DD.MM.YYYY): ";
		cin >> hire_date;
		try {
			Correct_Date(hire_date); // Проверка корректности даты
			break;
		}
		catch (const Data_Exception& e) {
			cout << "Ошибка: " << e.what() << endl;
		}
	}
}

void Manager::Hire_Employ_Next_Part(Workers* worker) {
	string name, hire_date, job_title;
	int age, salary, work_experience, stress_level;
	cout << "Введите имя: ";
	cin >> name;
	Check_Age(age);
	Check_Salary(salary);
	Check_Hire_Date(hire_date);
	cout << "Введите должность: ";
	cin >> job_title;
	Check_Work_Expirience(work_experience);
	Check_Stress_Level(stress_level);

	worker->Set_Name(name);
	worker->Set_Age(age);
	worker->Set_Salary(salary);
	worker->Set_Job_Title(job_title);
	worker->Set_Work_Experience(work_experience);
	worker->Set_Stress_Level(stress_level);
	worker->Set_Hired_Status(true);
	worker->Set_Object_Info();
}

void Manager::Choosed_Worker_2(const int& choice, Workers* worker1, Workers* worker2, Workers* worker3, Workers* worker4) {
	switch (choice) {
	case 1:
		if (worker1->Get_Hired_Status()) cout << "Эта должность уже занята\n";
		else Hire_Employ_Next_Part(worker1);
		break;
	case 2:
		if (worker2->Get_Hired_Status()) cout << "Эта должность уже занята\n";
		else Hire_Employ_Next_Part(worker2);
		break;
	case 3:
		if (worker3->Get_Hired_Status()) cout << "Эта должность уже занята\n";
		else Hire_Employ_Next_Part(worker3);
		break;
	case 4:
		if (worker2->Get_Hired_Status()) cout << "Эта должность уже занята\n";
		else Hire_Employ_Next_Part(worker2);
		break;
	default:
		cout << "Такого варианта нет" << endl;
	}
}

void Manager::Choosed_Worker(const int& choice, Workers* worker1, Workers* worker2, Workers* worker3, Workers* worker4) {
	switch (choice) {
	case 1:
		worker1->Set_Hired_Status(false);
		cout << "Уволен: " << worker1->Get_Name() << endl << endl;
		break;
	case 2:
		worker2->Set_Hired_Status(false);
		cout << "Уволен: " << worker2->Get_Name() << endl << endl;
		break;
	case 3:
		worker3->Set_Hired_Status(false);
		cout << "Уволен: " << worker3->Get_Name() << endl << endl;
		break;
	case 4:
		worker4->Set_Hired_Status(false);
		cout << "Уволен: " << worker4->Get_Name() << endl << endl;
		break;
	default:
		cout << "Такого варианта нет" << endl;
	}
}

void Manager::Set_Object_Info() {
	cout << "\nИмя лучшего сотрудника месяца: \n";
	cin >> worker_of_month;
}

void Manager::Print() const {
	cout << endl << "Worker of month: " << worker_of_month << endl;
}

Manager::Manager(string worker_of_month, int salary, string hire_date, string job_title, int work_experience,
	int stress_level, string name, int age)
	: worker_of_month(worker_of_month), Workers(salary, hire_date, job_title, work_experience, stress_level, name, age) {}

void Manager::Hire_Employ(Workers* worker1, Workers* worker2, Workers* worker3, Workers* worker4) {
	int choice;
	cout << "1. Автор" << endl;
	cout << "2. Уборщик" << endl;
	cout << "3. Кассир" << endl;
	cout << "4. Разнорабочий" << endl;
	while (true) {
		cout << "Введите номер работника, которого хотите нанять: ";
		cin >> choice;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (choice < 0 || choice > 4) throw Value_Exception("Некорректный выбор ");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}
	cout << endl;
	Choosed_Worker_2(choice, worker1, worker2, worker3, worker4);
}

void Manager::Fire_Employ(Workers* worker1, Workers* worker2, Workers* worker3, Workers* worker4) {
	int choice;
	cout << "1. Автор" << endl;
	cout << "2. Уборщик" << endl;
	cout << "3. Кассир" << endl;
	cout << "4. Разнорабочий" << endl;
	while (true) {
		cout << "Введите номер работника, которого хотите уволить: ";
		cin >> choice;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
			continue;
		}
		try {
			if (choice < 0 || choice > 4) throw Value_Exception("Некорректный выбор ");
			break;
		}
		catch (const Value_Exception& e) {
			cout << e.what() << endl;
		}
	}
	cout << endl;
	Choosed_Worker(choice, worker1, worker2, worker3, worker4);
}