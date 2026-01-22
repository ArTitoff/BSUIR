#include "Data_Exception.h"

void  Correct_Date(string& pub_date) {
    if (pub_date.size() != 10 || pub_date[2] != '.' || pub_date[5] != '.')
        throw Data_Exception("Некорректный ввод даты. Ожидалось: DD.MM.YYYY");

    int date, month, year;
    char dot1, dot2;
    stringstream ss(pub_date);
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