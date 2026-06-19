// Выполнил студент группы 321703 БГУИР:
// - Титов Артём Вадимович
// Вариант 14
//
// Строка для хранения логического выражения
// 06.03.2024
//
// Источники:
// - Логические основы интеллектуальных систем. Практикум: учебно-методическое пособие / В. В. Голенков, В. П. Ивашенко,
// Д. Г. Колб, К. А. Уваров. – Минск: БГУИР, 2011.
//Задача:
//Определить является ли формула КНФ

#include <iostream>
#include <string> 
#include <vector>

using namespace std;

bool is_operand(char operand) {
	bool value = operand == '(' || operand == ')' || operand == '/' || operand == '\\' || operand == '!';
	return value;
}

bool is_symbol(char symbol) {
	bool value = symbol >= 65 && symbol <= 90;
	return value;
}

bool valid_alphabet(string str) {
	for (int i = 0; i < str.size(); i++) {
		if (is_operand(str[i]) || is_symbol(str[i]))
			continue;
		else
			return false;
	}
	return true;
}

bool correct_substr_brackets_place(string str) {
	for (int i = 0; i < str.size();i++) {
		if (str[i] == '(') {
			int brackets_count = 0;
			int index = 0;
			for (int j = i; j < str.size(); j++) {
				if (str[j] == '(')
					++brackets_count;
				if (str[j] == ')')
					--brackets_count;
				if (brackets_count == 0) {
					index = j;
					break;
				}
			}
			brackets_count = 0;
			int sign_count = 0;
			for (int k = i; k < index; k++) {
				if (str[k] == '(')
					brackets_count++;
				if (str[k] == '!' || str[k] == '/')
					sign_count++;
			}
			if (sign_count != brackets_count)
				return false;
		}
	}
	return true;
} //((A/\A)/\A)

bool correct_brackets_count_for_all_knf(string str) {
	int brackets_count = 0;
	int close_brackets_count = 0;
	int sign_count = 0;
	for (int i = 0; i < str.size(); i++) {
		if (str[i] == '/' || str[i] == '!')
			sign_count++;
		else if (str[i] == '(')
			brackets_count++;
		else if (str[i] == ')')
			close_brackets_count++;
	}
	if (sign_count == 0) {
		return true;
	}
	if (sign_count != brackets_count)
		return false;
	if (brackets_count != close_brackets_count)
		return false;
	return true;
}

bool correct_one_symbol_writting(string str) {
	for (int i = 0; i < str.size(); i++) {
		if (is_symbol(str[i]) && i > 0 && str[i - 1] == ')') {
			return false;
		}
		if (is_symbol(str[i]) && i + 1 < str.size() &&
			(str[i + 1] == '(' || str[i + 1] == '!')) {
			return false;
		}
	}
	return true;
}

bool no_duplicate_or_one_subformula_brackets(string str) {
	for (int i = 0; i < str.size(); i++) {
		if (i > 0 && is_symbol(str[i]) && is_symbol(str[i - 1]))
			return false;
		if (i > 0 && i + 1 < str.size() && is_symbol(str[i]) && str[i - 1] == '(' && str[i + 1] == ')')
			return false;
	}
	return true;
}

bool main_brackets(string str) {
	int end_index = str.size() - 1;
	for (int i = 0; i < str.size(); i++) {
		if (str[i] == '/') {
			if (str[0] == '(' && str[end_index] == ')')
				return true;
			else
				return false;
		}
	}
	if (str[0] == '(' && str[1] != '!')
		return false;
	if (str.size() == 0)
		return false;
	return true; // (!A
}

bool correct_negation(string str) {
	for (int i = 0; i < str.size(); i++) {
		if (str[i] == '!') {
			if ((i > 0 && str[i - 1] == '(') && (i + 2 < str.size() && is_symbol(str[i + 1]) && str[i+2] == ')'))
				return true;
			else
				return false;
		}
	}
	return true;
}

bool empty_parentheses(string str) {
	for (int i = 0; i < str.size(); i++) {
		if (i + 1 < str.size() && ((str[i] == '(' && str[i + 1] == ')') || (str[i] == ')' && str[i + 1] == '(')))
			return false;
	}
	return true;
}

vector<string> split_str(string str) {
	vector<string> split_str;
	int index = 0;
	for (int i = 0; i < str.size(); i++) {
		if (str[i] == '/' && str[i + 1] == '\\') {
			string sub_str = "";
			for (int j = index; j < i; j++)
				sub_str += str[j];
			split_str.push_back(sub_str);
			index = i + 2;
		}
	}
	string sub_str = "";
	for (int k = index; k < str.size(); k++)
		sub_str += str[k];
	split_str.push_back(sub_str);
	return split_str;
}

bool correct_substr_without_conjuction(string str) { //(A/\(B\/D))
	int open_bracket_count = 0;
	int close_bracket_count = 0;
	int sign_count = 0;
	for (int i = 0; i < str.size(); i++) {
		if (str[i] == '(')
			open_bracket_count++;
		if (str[i] == ')')
			close_bracket_count++;
		if (str[i] == '/' || str[i] == '!')
			sign_count++;
	}
	if (sign_count == 0)
		return true;
	if (open_bracket_count > close_bracket_count && close_bracket_count != sign_count)
		return false;
	if (open_bracket_count < close_bracket_count && open_bracket_count != sign_count)
		return false;
	return true;
}

bool good_disjuction(string str) {
	for (int i = 0; i < str.size(); i++) {
		if (str[i] == '\\' && (i == 0 || i + 1 >= str.size()))
			return false;
		if (str[i] == '\\' && i > 0 && i + 2 < str.size()) {
			if ((str[i + 1] == '/' && (str[i - 1] == ')' || is_symbol(str[i - 1]))
				&& (str[i + 2] == '(' || is_symbol(str[i + 2]) || str[i + 3] == '!')) ||
				(str[i - 1] == '/' && (is_symbol(str[i + 1]) || str[i + 1] == '(' ))) {
				continue;
			}
			else {
				return false;
			}
		}
	}
	return true;
}

bool good_conjuction(string str) {
	for (int i = 0; i < str.size(); i++) {
		if (str[i] == '/' && (i == 0 || i + 2 >= str.size())) {
			return false;
		}
			
		if (str[i] == '/' && i > 0 && i + 2 < str.size()) {
			if ((str[i + 1] == '\\' && (is_symbol(str[i - 1]) || str[i - 1] == ')')
				&& (is_symbol(str[i + 2]) || str[i + 2] == '(')) ||
				(str[i - 1] == '\\' && (is_symbol(str[i + 1]) || str[i + 1] == '('))) {
				continue;
			}
			else {
				return false;
			}
		}
	}
	return true;
}

void is_knf() {
	string str;
	cout << "\nВведите КНФ: ";
	cin.ignore();
	getline(cin, str);
	if (!valid_alphabet(str)){
		cout << "\nФормула НЕ является КНФ!\n";// Алфавит\n";
		return;
	}
	else if (!correct_brackets_count_for_all_knf(str))
	{
		cout << "\nФормула НЕ является КНФ! Скобки\n";
		return;
	}
	else if (!main_brackets(str))
	{
		cout << "\nФормула НЕ является КНФ! Главные скобки\n";
		return;
	}
	else if (!correct_negation(str))
	{
		cout << "\nФормула НЕ является КНФ!\n";
		return;
	}
	else if (!no_duplicate_or_one_subformula_brackets(str))
	{
		cout << "\nФормула НЕ является КНФ! Дубликат или скобки\n";
		return;
	}
	else if (!correct_one_symbol_writting(str))
	{
		cout << "\nФормула НЕ является КНФ! Один сивол\n";
		return;
	}
	else if (!empty_parentheses(str))
	{
		cout << "\nФормула НЕ является КНФ! Пустые скобки\n";
		return;
	}
	else if (!correct_substr_brackets_place(str))
	{
		cout << "\nФормула НЕ является КНФ!\n";
		return;
	}
	else if (!good_disjuction(str))
	{
		cout << "\nФормула НЕ является КНФ! Дизъюнкция\n";
		return;
	}
	else if (!good_conjuction(str))
	{
		cout << "\nФормула НЕ является КНФ! Конъюнкиця\n";
		return;
	}
	else {
		vector<string> splited_str = split_str(str);
		for (int i = 0; i < splited_str.size(); i++) {
			//cout << splited_str[i];
			if (!correct_substr_without_conjuction(splited_str[i])) {
				cout << "\nФормула НЕ является КНФ! \n";
				return;
			}
		} // ((A/\A)/\(B\/1))
	}
	cout << "\nФормула является КНФ!\n\n";
}

int main()
{
	setlocale(LC_ALL, "RU");
	int choice;

	while (true) {

		cout << "Если желаете продолжить, нажмите 1. Если выйти - нажмите 0: ";
		cin >> choice;

		if (cin.fail()) {
			cin.clear(); 
			cin.ignore(numeric_limits<streamsize>::max(), '\n'); 
			cout << "Пожалуйста, введите корректное целое число." << endl;
			continue; 
		}
		if (choice == 0) 
			break;
		if (choice == 1)
			is_knf();
	}
	return 0;
}
