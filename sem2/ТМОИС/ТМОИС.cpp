
#include<vector>
#include <iostream>
using namespace std;



int main()
{
    setlocale(LC_ALL, "RU");
    int vibor, moshA, moshB, moshC = 0, valE = 0, valD = 0;
    cout << "Выберите способ задания множества: перечисление(1) или высказыванием(2)\n";    //Bыбор способа задания множества
    cin >> vibor;
    cout << "Введите мощность множества A: ";    //Пользователь задает мощность первого множества
    cin >> moshA;
    int* A = new int[moshA];
    if (vibor == 1) {              //Перечисление

        cout << "Введите элементы множества A: ";
        for (int i = 0; i < moshA; i++) {        // Пользователь задает первое множество
            cin >> A[i];
        }
    }
    else if (vibor == 2) {                //Bысказывание    
        int x = 1;
        for (int i = 0; i < moshA; i++) {        // Задание первого множества высказыванием
            A[i] = pow(-1, x + 1);
            x++;
        }
    }

    cout << "Введите мощность множества B: ";    //Пользователь задает мощность второго множества
    cin >> moshB;
    int* B = new int[moshB];
    if (vibor == 1) {              //Перечисление

        cout << "Введите элементы множества B: ";
        for (int i = 0; i < moshB; i++) {        //Пользователь задает второе множество
            cin >> B[i];
        }
    }
    else if (vibor==2){
        int x = 1;
        for (int i = 0; i <= moshB; i++) {        // Пользователь задает второе множество
            B[i] = pow(x, 2) - 10 * x;
            x++;
        }
    }




    int k = -200;
   
    
    int* C = new int[moshA + moshB];
    int* D = new int[moshA];
    int* E = new int[moshB];
    int Ab[400];
    int U[401];
    for (int i = 0; i < 401; i++) {
        U[i] = k;
        k++;
    }
    

 

    cout << "Выберите операцию над множествами: объединение A и B(1), пересечение A и B(2), разность A и B(3), разность B и A(4), симметрическую разность A и B(5), декартово произведение A и B(6), декартово произведение B и A(7), дополнение A(8), дополнение B(9)\n ";
    cin >> vibor;          //Выбор операции
    switch (vibor) {
    case 1:              //Объединение

        for (int i = 0; i < moshA; i++) {
            bool isDuplicate = false;
            for (int j = 0; j < moshC; j++) { //Переносим все элементы множества A в множество C.
                if (A[i] == C[j]) {
                    isDuplicate = true;
                    break;
                }
            }
            if (!isDuplicate) {
                C[moshC] = A[i];
                moshC++;
            }
        }

        for (int i = 0; i < moshB; i++) {      //Сравниваем поочередно элементы множеств
            bool isDuplicate = false;
            for (int j = 0; j < moshC; j++) {
                if (B[i] == C[j]) {
                    isDuplicate = true;        //Если равен, то берем следующий
                    break;
                }
            }
            if (!isDuplicate) {            //Если не равен ни одному элементу B, то добавляем в множество C
                C[moshC] = B[i];
                moshC++;
            }
        }
        break;

    case 2:                      //Пересечение
        for (int i = 0; i < moshA; i++) {      //Берем первый элемент А
            for (int j = 0; j < moshB; j++) {    //Берем первый элемент В 
                if (A[i] == B[j]) {
                    C[moshC] = A[i];
                    moshC++;
                    break;              //Если найден одинаковый элемент, добавляем в множество C
                }
            }                    //Берем следующий эл В
        }                      //Берем следующий эл А
        break;

    case 3:                    //Разность A и B
        for (int i = 0; i < moshA; i++) {    //Берем первый элемент А
            bool isduplicate = false;
            for (int j = 0; j < moshB; j++) {  //Берем первый элемент В 
                if (A[i] == B[j]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент А не равен ни одному элменту В, то записываем его в С
                C[moshC] = A[i];
                moshC++;
            }
        }                    //Берем следующий эл А
        break;

        
    case 4:                    //Разность B и A
        for (int i = 0; i < moshB; i++) {    //Берем первый элемент В 
            bool isduplicate = false;
            for (int j = 0; j < moshA; j++) {  //Берем первый элемент А
                if (B[i] == A[j]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл А
            if (!isduplicate) {          //Если элемент В не равен ни одному элменту А, то записываем его в С
                C[moshC] = B[i];
                moshC++;
            }
        }                    //Берем следующий эл В
        break;

    case 5:                    //Симметрическая разность множеств A и B 

        for (int i = 0; i < moshA; i++) {    //Разность A и B
            bool isduplicate = false;
            for (int j = 0; j < moshB; j++) {
                if (A[i] == B[j]) {
                    isduplicate = true;  break;
                }
            }
            if (!isduplicate) {
                D[valD] = A[i];
                valD++;
            }
        }

        for (int i = 0; i < moshB; i++) {    //Разность B и A
            bool isduplicate = false;
            for (int j = 0; j < moshA; j++) {
                if (B[i] == A[j]) {
                    isduplicate = true;  break;
                }
            }
            if (!isduplicate) {
                E[valE] = B[i];
                valE++;
            }
        }

        for (int i = 0; i < valE; i++) {    //Объединение 
            bool isDuplicate = false;
            for (int j = 0; j < moshC; j++) {
                if (E[i] == C[j]) {
                    isDuplicate = true;
                    break;
                }
            }
            if (!isDuplicate) {
                C[moshC] = E[i];
                moshC++;
            }
        }

        for (int i = 0; i < valD; i++) {
            bool isDuplicate = false;
            for (int j = 0; j < moshC; j++) {
                if (D[i] == C[j]) {
                    isDuplicate = true;
                    break;
                }
            }
            if (!isDuplicate) {
                C[moshC] = D[i];
                moshC++;
            }
        } break;

    case 6:
        moshC = -1;
        cout << "C = {";
        for (int i = 0; i < moshA; i++) {    //Берем первый элемент А и присваеваем его значение а
            for (int j = 0; j < moshB; j++) {    //Берем первый элемент В и присваеваем его значение b
                cout << '<' << A[i] << ',' << B[j] << "> ";  //Присваеваем элементам кортежа значения a и b
            }                    //Берем следующий эл А
        }                      //Берем следующий эл В
        cout << "}";
        break;


    case 7:
        moshC = -1;
        cout << "C = {";
        for (int i = 0; i < moshB; i++) {    //Берем первый элемент В и присваеваем его значение b
            for (int j = 0; j < moshA; j++) {    //Берем первый элемент А и присваеваем его значение а
                cout << '<' << B[i] << ',' << A[j] << "> ";    //Присваеваем элементам кортежа значения a и b
            }                    //Берем следующий эл В
        }                      //Берем следующий эл А
        cout << "}";
        break;


    case 8:                    //Дополнение А
      
        for (int i = 0; i < 401; i++) {    //Берем первый элемент А
            bool isduplicate = false;
            for (int j = 0; j < moshA; j++) {  //Берем первый элемент В 
                if (U[i] == A[j]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент А не равен ни одному элменту В, то записываем его в С
                Ab[moshC] = U[i];
                moshC++;
            }
        }

        break;

    case 9:                    //Дополнение А

        for (int i = 0; i < 401; i++) {    //Берем первый элемент А
            bool isduplicate = false;
            for (int j = 0; j < moshB; j++) {  //Берем первый элемент В 
                if (U[i] == B[j]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент А не равен ни одному элменту В, то записываем его в С
                Ab[moshC] = U[i];
                moshC++;
            }
        }

        break;
 

    }
    if (moshC == 0) {
        cout << "C - пустое множество";
    }
    else if (vibor == 8)
    {
        for (int i = 0; i < moshC; i++) {        //Вывод множества С пользователю

            cout << Ab[i] << " ";
        }
    }
    else if (vibor == 9)
    {
        for (int i = 0; i < moshC; i++) {        //Вывод множества С пользователю

            cout << Ab[i] << " ";
        }
    }
    else {
        for (int i = 0; i < moshC; i++) {        //Вывод множества С пользователю

            cout << C[i] << " ";
        }
    }

    return 0;
}