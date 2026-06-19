#include "Handyman.h"


int main() {
	setlocale(LC_ALL, "RU");
	Visitor man1("Goal", 16, "Shon", 23);
	Visitor man2("", 16, "Rob", 23);
	Visitor man3("", 16, "Kerl", 23);
	Orchestra orchestra(true, 120, 9.5, "Классическая музыка", "Вечерний оркестр", 30, 5, "23.10.2024", "Великолепный вечер классической музыки.");
	// Добавление актеров в оркестр
	Musician muz1("Солист", 5000, "22.10.2020", "Музыкант", 5, 3, "Иван", 30);
	Musician muz2("Гитарист", 4500, "17.09.2021", "Музыкант", 4, 2, "Федя", 28);
	orchestra.Add_Musician(muz1);
	orchestra.Add_Musician(muz2);
	vector<string> decor = { "Декорация 1", "Декорация 2", "Декорация 3" };
	Performance performance(decor, 90, 8, "Драма", "Потеря потерь", 6, 7, "24.10.2024", "Самое трагическое, что вы когда либо видели");
	Actor act1("Комические роли", 4500, "17.09.2021", "Актер", 4, 2, "Федя", 28);
	performance.Add_Actor(act1);
	Theater theater;
	theater.Add_Orchestra(orchestra);
	theater.Add_Performance(performance);
	theater.List_of_Events();
	theater.Show_Event_Info();

	vector<string> works = { "Book 1", "Book 2", "Book 3" };
	Author author(works, 60000, "01.12.2023", "Writer", 10, 2, "Bob", 35);
	
	author.Info();
	Cleaner cli(works, 60000, "01.11.2023", "Cleaner", 10, 2, "Mark", 35);
	Chashier chais(60000, "30.06.2023", "Chashier", 10, 2, "Lorry", 35, 5, 5, 3, 6, 12, 15);
	Handyman han(60000, "01.04.2023", "Handyman", 10, 2, "Hank", 35);
	Manager man(author.Get_Name(), 60000, "07.04.2019", "Manager", 10, 2, "Bobsy", 35);
	man.Print();

	chais.Book_For_Visitor(man1, 1, 1, 1);
	chais.Book_For_Visitor(man2, 1, 1, 1);
	chais.Book_For_Visitor(man3, 3, 3, 1);

	cout << endl;
	theater.Menu(man, chais, author, cli, han);

	return 0;
}