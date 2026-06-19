#include <iostream>
#include <cmath>

using namespace std;
int main()
{
    setlocale(LC_ALL, "RU");

    double a, x, y, s,f;
    int k;
    cout << "Введите x - ";
    cin >> x;
    cout << "Введите y - ";
    cin >> y;
    cout << "Введите функцию f на выбор: 1- sh(x), 2- x^2, 3- exp(x)  ";
    cin >> k ;
    switch (k) {
    case 1: f = sinh(x); break;
    case 2: f = pow(x, 2); break;
    case 3: f = exp(x); break;
    default: cout << "Не выбрана функция"; return 1;
    }
    a = pow(x, 3);
    if (a > 0)
        s = pow(log(f), 3);
    else if (a < 0)
        s = tan(pow(x, 3)) + f;
    else s = pow(fabs(pow(y, 3) - pow(x, 2)), 1 / 3.);
    
    cout << "Результат" << s;
    return 0;
}
