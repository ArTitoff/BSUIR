// PPOIS_1.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include "Header.h"

int main()
{
    setlocale(LC_ALL, "RU");
    Piatnashky example;
    int index;
    do {
        cout << "Введите номер ячейки, которую хотите просмотреть ";
        cin >> index;
        if(cin.fail()){
        cin.clear();
        cin.ignore(32767, '\n');
        cout << "NECOOR VVOD";
        return -1;
        }
    } while (index < 0 && index > 16);
    int a = example[index-1];
    cout << a << " - значение из выбранной ячейки\n\n";
    cout << "Новая игра\n\n";
    example.Play(); 
}

