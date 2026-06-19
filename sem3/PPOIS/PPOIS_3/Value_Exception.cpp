#include "Value_Exception.h"

void  Correct_Cin(int& param, int value1, int value2) {
    while (true) {
        cout << "Введите значение: ";
        cin >> param;

        // Проверка на некорректный ввод
        if (cin.fail()) {
            cin.clear(); // Сброс состояния потока
            cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Очистка буфера
            cout << "Ошибка: Введено не число. Попробуйте еще раз." << endl;
            continue; // Возврат к началу цикла
        }
        try {
            if (param < value1 || param > value2) throw Value_Exception("Некорректный ввод");
            break; // Если возраст корректен, выходим из цикла
        }
        catch (const Value_Exception& e) {
            cout << e.what() << endl; // Вывод сообщения об ошибке
        }
    }
}