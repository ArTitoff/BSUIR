#include "Performance.h"

void Performance::Add_Actor(Actor& actor) {
	actors.push_back(actor);
}

Performance::Performance(vector<string> decorations, int duration, double rating, string genre, string show_name, int member_amount,
	int rehearsals_count, string premiere_date, string description) :
	decorations(decorations), Event(duration, rating, genre, show_name, member_amount, rehearsals_count, premiere_date, description) {}

void Performance::Print_Info() const {
	cout << "Название: " << show_name << endl;
	cout << "Дата премьеры: " << premiere_date << endl;
	cout << "Продолжительность: " << duration << " минут" << endl;
	cout << "Рейтинг: " << rating << endl;
	cout << "Жанр: " << genre << endl;
	cout << "Количество участников: " << member_amount << endl;
	cout << "Количество репетиций: " << rehearsals_count << endl;
	cout << "Описание: " << description << endl;
	cout << "Декорации: ";
	for (int i = 0; i < decorations.size(); i++) {
		cout << decorations[i] << " ";
	}
	if (actors.size() != 0) {
		for (int i = 0; i < actors.size(); i++)
			cout << "\nИмя: " << actors[i].Get_Name() << "  Роль: " << actors[i].Get_Role();
	}
	else cout << "Актеров не будет\n";
	cout << endl << endl;
}

string Performance::Get_Show_Name() const {
	return show_name;
}

string Performance::Get_Premiere_Date() const {
	return premiere_date;
}