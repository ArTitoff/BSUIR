#include "Orchestra.h"

Orchestra::Orchestra(bool conductor, int duration, double rating, string genre, string show_name, int member_amount,
	int rehearsals_count, string premiere_date, string description) :
	conductor(conductor), Event(duration, rating, genre, show_name, member_amount, rehearsals_count, premiere_date, description) {}

void Orchestra::Add_Musician(Musician& musician) {
	musicians.push_back(musician);
}

string Orchestra::Get_Show_Name() const {
	return show_name;
}

string Orchestra::Get_Premiere_Date() const {
	return premiere_date;
}

void Orchestra::Print_Info() const {
	cout << "Название: " << show_name << endl;
	cout << "Дата премьеры: " << premiere_date << endl;
	cout << "Продолжительность: " << duration << " минут" << endl;
	cout << "Рейтинг: " << rating << endl;
	cout << "Жанр: " << genre << endl;
	cout << "Количество участников: " << member_amount << endl;
	cout << "Количество репетиций: " << rehearsals_count << endl;
	cout << "Описание: " << description << endl;
	cout << "Дирижер: " << (conductor ? "У оркестра есть дирижер" : "Оркестр играет без дирижера") << endl;
	if (musicians.size() != 0) {
		for (int i = 0; i < musicians.size(); i++)
			cout << "\nИмя: " << musicians[i].Get_Name() << "  Инструмент: " << musicians[i].Get_Playing_Insrument();
	}
	else cout << "Музыкантов не будет\n";
	cout << endl << endl;
}