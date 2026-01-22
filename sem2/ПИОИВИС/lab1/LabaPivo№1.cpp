#include <iostream>
#include "Mnozhestva.h"
#include <locale.h>
using namespace std;


int main() {
	setlocale(LC_ALL, "RU");
	Branch* root4 = nullptr;
	Branch* root3 = nullptr;
	Branch* root = nullptr;
	Branch* root2 = nullptr;
	root4 = root;
	Add(root, 5);
	Add(root, 15);
	Add(root, rand() % 100);
	cout << "Вывод множества A: " << endl;
	
	print(root);

	cout << endl;
	Add(root2, 52);
	Add(root2, 15);
	Add(root2, rand() % 100);
	cout << endl << "Вывод множества B: " << endl;
	print(root2);
	
	Peresechenie(root, root2, root3);
	cout << endl << endl << "Пересечение A и B" << endl;
	print(root3);

	Objedinenie(root, root2, root4);
	cout << endl << endl << "Объединение  A и B" << endl;
	print(root4);

	cout << endl << endl << "Поиск элемента 41" << endl;
	FindElem(root4, 41);
	cout << endl << endl << "Поиск элемента 24" << endl;
	FindElem(root4, 24);

	cout << endl << endl << "Удаление элемента 41" << endl;
	removeNode(root4, 41);
	print(root4);

	
	return 0;
}