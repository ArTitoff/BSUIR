
#include<vector>
#include <iostream>
using namespace std;



int main()
{
    setlocale(LC_ALL, "RU");
    int vibor, moshA, moshX, moshY, moshU, moshV, moshB, moshC = 0, valE = 0, valD = 0;
    int moshC_1 = 0, valE_1 = 0, valD_1 = 0, moshC_2 = 0, valE_2 = 0, valD_2 = 0;


    cout << "Способ задания - перечисление\n";
    cout << "Соответствие A:\n";
    cout << "   Введите мощность области отпарвления X: ";    //Пользователь задает мощность области отпарвления
    cin >> moshX;
    int* X = new int[moshX]; //создаем обл отправления
    cout << "      Введите элементы области отпарвления X: ";
    for (int i = 0; i < moshX; i++)
        cin >> X[i];


    cout << "   Введите мощность области прибытия Y: ";    //Пользователь задает мощность области прибытия
    cin >> moshY;
    int* Y = new int[moshY]; //создаем обл прибытия
    cout << "      Введите элементы области прибытия Y: ";
    for (int i = 0; i < moshY; i++)
        cin >> Y[i];

    cout << "   Введите мощность графика G: ";    //Пользователь задает мощность элементы графика G
    cin >> moshA;
    int** A = new int* [moshA];
    for (int i = 0; i < moshA; i++) {
        A[i] = new int[2];
    }

    
    cout << "      Введите элементы графика G: ";
    for (int i = 0; i < moshA; i++) {        // Пользователь задает элементы графика G
        for (int j = 0; j < 2; j++) {
            cin >> A[i][j];
        }
    }




    cout << "Соответствие B:\n";
    cout << "   Введите мощность области отпарвления U: ";    //Пользователь задает мощность второй области отпарвления
    cin >> moshU;
    int* U = new int[moshU]; //создаем обл отправления
    cout << "      Введите элементы области отпарвления U: ";
    for (int i = 0; i < moshU; i++)
        cin >> U[i];


    cout << "   Введите мощность области прибытия V: ";    //Пользователь задает мощность второй области прибытия
    cin >> moshV;
    int* V = new int[moshV]; //создаем обл прибытия
    cout << "      Введите элементы области прибытия V: ";
    for (int i = 0; i < moshV; i++)
        cin >> V[i];

    cout << "   Введите мощность графика F: ";    //Пользователь задает мощность второго графика
    cin >> moshB;
    int** B = new int* [moshB];
    for (int i = 0; i < moshB; i++) {
        B[i] = new int[2];
    }


    cout << "      Введите элементы графика F: ";
    for (int i = 0; i < moshB; i++) {        //Пользователь задает второй график
        for (int j = 0; j < 2; j++) {
            cin >> B[i][j];
        }
    }



    int* C_1 = new int[moshX + moshY];          //для работы с областями 
    int* D_1 = new int[moshX];
    int* E_1 = new int[moshY];

    int* C_2 = new int[moshU + moshV];
    int* D_2 = new int[moshU];
    int* E_2 = new int[moshV];

    int x = -200;


    int** C = new int* [moshA + moshB];         //для работы с графиками
    for (int i = 0; i < moshA + moshB; i++) {
        C[i] = new int[2];
    }



    int** C_3 = new int* [100];         //для работы с графиками
    for (int i = 0; i < 100; i++) {
        C_3[i] = new int[2];
    }

    int** D = new int* [moshA];
    for (int i = 0; i < moshA; i++) {
        D[i] = new int[2];
    }
    int** E = new int* [moshB];
    for (int i = 0; i < moshB; i++) {
        E[i] = new int[2];
    }


    int** Un = new int* [150];
    for (int i = 0; i < 150; i++) {
        Un[i] = new int[2];
    }

    int i = 0;
    for (int x = 1; x < 11; x++) {
        int y = 1;
        for (y; y < 11; y++) {
            Un[i][0] = x;
            Un[i][1] = y;
            i++;
        }
    }

    int k_1 = -200, k_2 = -200;
    int Un_1[401];
    for (int i = 0; i < 401; i++) {
        Un_1[i] = k_1;
        k_1++;
    }

    int Un_2[401];
    for (int i = 0; i < 401; i++) {
        Un_2[i] = k_2;
        k_2++;
    }
    int Ab_1[400];
    int Ab_2[400];
    cout << "Выберите операцию над множествами:\n объединение A и B(1),\n пересечение A и B(2),\n разность A и B(3),\n разность B и A(4),\n симметрическую разность A и B(5),\n дополнение А(6),\n дополнение В(7),\n инверсия А(8),\n инверсия B(9),\n композиция А и В(10) ,\n композиция В и А(11)\n ";
    cout << "образ A (12),\n образ B (13),\n прообраз A (14),\n прообраз B (15),\n сужение A (16),\n сужение B (17),\n продолжение А (18),\n продолжение B (19),\n";
    cin >> vibor;          //Выбор операции
    switch (vibor) {
    case 1:              //Объединение

        for (int i = 0; i < moshX; i++) {
            bool isDuplicate = false;
            for (int j = 0; j < moshC_1; j++) { //Переносим все элементы множества A в множество C.
                if (X[i] == C_1[j]) {
                    isDuplicate = true;
                    break;
                }
            }
            if (!isDuplicate) {
                C_1[moshC_1] = X[i];
                moshC_1++;
            }
        }

        for (int i = 0; i < moshU; i++) {      //Сравниваем поочередно элементы множеств
            bool isDuplicate = false;
            for (int j = 0; j < moshC_1; j++) {
                if (U[i] == C_1[j]) {
                    isDuplicate = true;        //Если равен, то берем следующий
                    break;
                }
            }
            if (!isDuplicate) {            //Если не равен ни одному элементу B, то добавляем в множество C
                C_1[moshC_1] = U[i];
                moshC_1++;
            }
        }

        for (int i = 0; i < moshY; i++) {
            bool isDuplicate = false;
            for (int j = 0; j < moshC_2; j++) { //Переносим все элементы множества A в множество C.
                if (Y[i] == C_2[j]) {
                    isDuplicate = true;
                    break;
                }
            }
            if (!isDuplicate) {
                C_2[moshC_2] = Y[i];
                moshC_2++;
            }
        }

        for (int i = 0; i < moshV; i++) {      //Сравниваем поочередно элементы множеств
            bool isDuplicate = false;
            for (int j = 0; j < moshC_2; j++) {
                if (V[i] == C_2[j]) {
                    isDuplicate = true;        //Если равен, то берем следующий
                    break;
                }
            }
            if (!isDuplicate) {            //Если не равен ни одному элементу B, то добавляем в множество C
                C_2[moshC_2] = V[i];
                moshC_2++;
            }
        }

        /////
        for (int i = 0; i < moshA; i++) {
            bool isDuplicate = false;
            for (int j = 0; j < moshC; j++) { //Переносим все элементы множества A в множество C.
                if (A[i][0] == C[j][0] && A[i][1] == C[j][1]) {
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
                if (B[i][0] == C[j][0] && B[i][1] == C[j][1]) {
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

        for (int i = 0; i < moshX; i++) {      //Берем первый элемент А
            for (int j = 0; j < moshU; j++) {    //Берем первый элемент В 
                if (X[i] == U[j]) {
                    C_1[moshC_1] = X[i];
                    moshC_1++;
                    break;              //Если найден одинаковый элемент, добавляем в множество C
                }
            }                    //Берем следующий эл В
        }

        for (int i = 0; i < moshY; i++) {      //Берем первый элемент А
            for (int j = 0; j < moshV; j++) {    //Берем первый элемент В 
                if (Y[i] == V[j]) {
                    C_2[moshC_2] = Y[i];
                    moshC_2++;
                    break;              //Если найден одинаковый элемент, добавляем в множество C
                }
            }                    //Берем следующий эл В
        }

        //////
        for (int i = 0; i < moshA; i++) {      //Берем первый элемент А
            for (int j = 0; j < moshB; j++) {    //Берем первый элемент В 
                if (A[i][0] == B[j][0] && A[i][1] == B[j][1]) {
                    C[moshC] = A[i];
                    moshC++;
                    break;              //Если найден одинаковый элемент, добавляем в множество C
                }
            }                    //Берем следующий эл В
        }                      //Берем следующий эл А
        break;

    case 3:                    //Разность A и B

        for (int i = 0; i < moshX; i++) {    //Берем первый элемент А
            bool isduplicate = false;
            for (int j = 0; j < moshU; j++) {  //Берем первый элемент В 
                if (X[i] == U[j]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент А не равен ни одному элменту В, то записываем его в С
                C_1[moshC_1] = X[i];
                moshC_1++;
            }
        }

        for (int i = 0; i < moshY; i++) {    //Берем первый элемент Y
            bool isduplicate = false;
            for (int j = 0; j < moshV; j++) {  //Берем первый элемент V
                if (X[i] == U[j]) {
                    isduplicate = true;  break;
                }
            }                  
            if (!isduplicate) {   
                C_2[moshC_2] = Y[i];
                moshC_2++;
            }
        }

        ////////

        for (int i = 0; i < moshA; i++) {    //Берем первый элемент А
            bool isduplicate = false;
            for (int j = 0; j < moshB; j++) {  //Берем первый элемент В 
                if (A[i][0] == B[j][0] && A[i][1] == B[j][1]) {
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

        for (int i = 0; i < moshU; i++) {    //Берем первый элемент U 
            bool isduplicate = false;
            for (int j = 0; j < moshX; j++) {  //Берем первый элемент X
                if (U[i] == X[j]) {
                    isduplicate = true;  break;
                }
            }                  
            if (!isduplicate) {          //Если элемент В не равен ни одному элменту А, то записываем его в С
                C_1[moshC_1] = U[i];
                moshC_1++;
            }
        }                    
        break;

        for (int i = 0; i < moshV; i++) {    //Берем первый элемент V 
            bool isduplicate = false;
            for (int j = 0; j < moshY; j++) {  //Берем первый элемент Y
                if (V[i] == Y[j]) {
                    isduplicate = true;  break;
                }
            }                  
            if (!isduplicate) {          
                C_2[moshC_2] = V[i];
                moshC_2++;
            }
        }                    //Берем следующий эл В
        break;


        ////
        for (int i = 0; i < moshB; i++) {    //Берем первый элемент В 
            bool isduplicate = false;
            for (int j = 0; j < moshA; j++) {  //Берем первый элемент А
                if (A[j][0] == B[i][0] && A[j][1] == B[i][1]) {
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

        for (int i = 0; i < moshX; i++) {    //Разность X и U
            bool isduplicate = false;
            for (int j = 0; j < moshU; j++) {
                if (X[i] == U[j]) {
                    isduplicate = true;  break;
                }
            }
            if (!isduplicate) {
                D_1[valD_1] = X[i];
                valD_1++;
            }
        }

        for (int i = 0; i < moshU; i++) {    //Разность U и X
            bool isduplicate = false;
            for (int j = 0; j < moshX; j++) {
                if (U[i] == X[j]) {
                    isduplicate = true;  break;
                }
            }
            if (!isduplicate) {
                E_1[valE_1] = U[i];
                valE_1++;
            }
        }

        for (int i = 0; i < valE_1; i++) {    //Объединение 
            bool isDuplicate = false;
            for (int j = 0; j < moshC_1; j++) {
                if (E_1[i] == C_1[j]) {
                    isDuplicate = true;
                    break;
                }
            }
            if (!isDuplicate) {
                C_1[moshC] = E_1[i];
                moshC_1++;
            }
        }

        for (int i = 0; i < valD_1; i++) {
            bool isDuplicate = false;
            for (int j = 0; j < moshC_1; j++) {
                if (D_1[i] == C_1[j]) {
                    isDuplicate = true;
                    break;
                }
            }
            if (!isDuplicate) {
                C_1[moshC] = D_1[i];
                moshC_1++;
            }
        } break;
        ///////

        for (int i = 0; i < moshY; i++) {    //Разность Y и V
            bool isduplicate = false;
            for (int j = 0; j < moshV; j++) {
                if (Y[i] == V[j]) {
                    isduplicate = true;  break;
                }
            }
            if (!isduplicate) {
                D_2[valD_2] = Y[i];
                valD_2++;
            }
        }

        for (int i = 0; i < moshV; i++) {    //Разность V и Y
            bool isduplicate = false;
            for (int j = 0; j < moshY; j++) {
                if (V[i] == Y[j]) {
                    isduplicate = true;  break;
                }
            }
            if (!isduplicate) {
                E_2[valE_2] = V[i];
                valE_2++;
            }
        }

        for (int i = 0; i < valE_2; i++) {    //Объединение 
            bool isDuplicate = false;
            for (int j = 0; j < moshC_2; j++) {
                if (E_2[i] == C_2[j]) {
                    isDuplicate = true;
                    break;
                }
            }
            if (!isDuplicate) {
                C_2[moshC_2] = E_2[i];
                moshC_2++;
            }
        }

        for (int i = 0; i < valD_2; i++) {
            bool isDuplicate = false;
            for (int j = 0; j < moshC_2; j++) {
                if (D_2[i] == C_2[j]) {
                    isDuplicate = true;
                    break;
                }
            }
            if (!isDuplicate) {
                C_2[moshC_2] = D_2[i];
                moshC_2++;
            }
        } break;


        ////////

        for (int i = 0; i < moshA; i++) {    //Разность A и B
            bool isduplicate = false;
            for (int j = 0; j < moshB; j++) {
                if (A[i][0] == B[j][0] && A[i][1] == B[j][1]) {
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
                if (A[j][0] == B[i][0] && A[j][1] == B[i][1]) {
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
                if (E[i][0] == C[j][0] && E[i][1] == C[j][1]) {
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
                if (D[i][0] == C[j][0] && D[i][1] == C[j][1]) {
                    isDuplicate = true;
                    break;
                }
            }
            if (!isDuplicate) {
                C[moshC] = D[i];
                moshC++;
            }
        } break;

    case 8: //инверсия А
        C_1 = Y;
        C_2 = X;
        moshC_1 = moshY;
        moshC_2 = moshX;
        for (int i = 0; i < moshA; i++) {
            C[moshC][1] = A[i][0];
            C[moshC][0] = A[i][1];
            moshC++;
        }
        break;
    case 9: //инверсия В
        C_1 = V;
        C_2 = U;
        moshC_1 = moshV;
        moshC_2 = moshU;
        for (int i = 0; i < moshB; i++) {
            C[moshC][1] = B[i][0];
            C[moshC][0] = B[i][1];
            moshC++;
        }
        break;

    case 10:    //композиция А и В
        C_1 = X;
        C_2 = V;
        moshC_1 = moshX;
        moshC_2 = moshV;
        for (int i = 0; i < moshA; i++) {
            for (int j = 0; j < moshB; j++) {
                if (A[i][1] == B[j][0]) {

                    bool isDuplicate = false;
                    for (int k = 0; k < moshC; k++) { //Переносим все элементы в множество C.
                        if (A[i][0] == C[k][0] && B[j][1] == C[k][1]) {
                            isDuplicate = true;
                            break;
                        }
                    }
                    if (!isDuplicate) {
                        C[moshC][0] = A[i][0];
                        C[moshC][1] = B[j][1];
                        moshC++;
                    }
                }

            }

        }
        break;

    case 11:    //композиция В и А
        C_1 = U;
        C_2 = Y;
        moshC_1 = moshU;
        moshC_2 = moshY;
        for (int i = 0; i < moshB; i++) {
            for (int j = 0; j < moshA; j++) {
                if (B[i][1] == A[j][0]) {


                    bool isDuplicate = false;
                    for (int k = 0; k < moshC; k++) { //Переносим все элементы в множество C.
                        if (A[i][1] == C[k][1] && B[i][0] == C[k][0]) {
                            isDuplicate = true;
                            break;
                        }
                    }
                    if (!isDuplicate) {
                        C[moshC][0] = B[i][0];
                        C[moshC][1] = A[j][1];
                        moshC++;
                    }
                }

            }

        }
        break;


    case 6:                  //Дополнение А


        for (int i = 0; i < 401; i++) {    //Берем первый элемент А
            bool isduplicate = false;
            for (int j = 0; j < moshX; j++) {  //Берем первый элемент В 
                if (Un_1[i] == X[j]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент А не равен ни одному элменту В, то записываем его в С
                Ab_1[moshC_1] = Un_1[i];
                moshC_1++;
            }
        }

        for (int i = 0; i < 401; i++) {    //Берем первый элемент А
            bool isduplicate = false;
            for (int j = 0; j < moshY; j++) {  //Берем первый элемент В 
                if (Un_2[i] == Y[j]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент А не равен ни одному элменту В, то записываем его в С
                Ab_2[moshC_2] = Un_2[i];
                moshC_2++;
            }
        }
        ////
        for (int i = 0; i < 100; i++) {    //Берем первый элемент U
            bool isduplicate = false;
            for (int j = 0; j < moshA; j++) {  //Берем первый элемент A 
                if (Un[i][0] == A[j][0] && Un[i][1] == A[j][1]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент U не равен ни одному элменту В, то записываем его в С
                C_3[moshC] = Un[i];
                moshC++;
            }
        }                    //Берем следующий эл А
        break;

    case 7:                  //Дополнение B

        for (int i = 0; i < 401; i++) {    //Берем первый элемент А
            bool isduplicate = false;
            for (int j = 0; j < moshU; j++) {  //Берем первый элемент В 
                if (Un_1[i] == U[j]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент А не равен ни одному элменту В, то записываем его в С
                Ab_1[moshC_1] = Un_1[i];
                moshC_1++;
            }
        }

        for (int i = 0; i < 401; i++) {    //Берем первый элемент А
            bool isduplicate = false;
            for (int j = 0; j < moshV; j++) {  //Берем первый элемент В 
                if (Un_2[i] == V[j]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент А не равен ни одному элменту В, то записываем его в С
                Ab_2[moshC_2] = Un_2[i];
                moshC_2++;
            }
        }
        ////
        for (int i = 0; i < 100; i++) {    //Берем первый элемент U
            bool isduplicate = false;
            for (int j = 0; j < moshB; j++) {  //Берем первый элемент В 
                if (Un[i][0] == B[j][0] && Un[i][1] == B[j][1]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент U не равен ни одному элменту В, то записываем его в С
                C_3[moshC] = Un[i];
                moshC++;
            }
        }                    //Берем следующий эл А
        break;

    case 12: //образ А
    {
        int moshM;
        cout << "   Введите мощность множества М: ";    //Пользователь задает мощность области отпарвления
        cin >> moshM;
        int* M = new int[moshM]; //создаем обл отправления
        cout << "      Введите элементы множества М: ";
        for (int i = 0; i < moshM; i++)
            cin >> M[i];

        for (int i = 0; i < moshA; i++) {
            bool isduplicate = false;
            for (int j = 0; j < moshM; j++) {
                if (A[i][0] == M[j]) {
                    isduplicate = true;
                    for (int k = 0; k < moshC_1; k++) {
                        if (C_1[k] == A[i][1]) {
                            isduplicate = false;  break;
                        }
                    }
                    break;
                }
            }
            if (isduplicate) {
                C_1[moshC_1] = A[i][1];
                moshC_1++;
            }
        }
        delete[] M;
        moshC = moshC_2 = 1;
    }
        break;
    

    case 13: //образ B
    {
        int moshM;
        cout << "   Введите мощность множества М: ";    //Пользователь задает мощность области отпарвления
        cin >> moshM;
        int* M = new int[moshM]; //создаем обл отправления
        cout << "      Введите элементы множества М: ";
        for (int i = 0; i < moshM; i++)
            cin >> M[i];

        for (int i = 0; i < moshB; i++) {
            bool isduplicate = false;
            for (int j = 0; j < moshM; j++) {
                if (B[i][0] == M[j]) {
                    isduplicate = true;
                    for (int k = 0; k < moshC_1; k++) {
                        if (C_1[k] == B[i][1]) {
                            isduplicate = false;  break;
                        }
                    }
                    break;
                }
            }
            if (isduplicate) {
                C_1[moshC_1] = B[i][1];
                moshC_1++;
            }
        }
        delete[] M;
        moshC = moshC_2 = 1;
    }
        break;
    
    case 14: //Прообраз А
    {
        int moshM;
        cout << "   Введите мощность множества М: ";    //Пользователь задает мощность области прибытия
        cin >> moshM;
        int* M = new int[moshM]; //создаем обл отправления
        cout << "      Введите элементы множества М: ";
        for (int i = 0; i < moshM; i++)
            cin >> M[i];

        for (int i = 0; i < moshA; i++) {
            bool isduplicate = false;
            for (int j = 0; j < moshM; j++) {
                if (A[i][1] == M[j]) {
                    isduplicate = true;
                    for (int k = 0; k < moshC_1; k++) {
                        if (C_1[k] == A[i][0]) {
                            isduplicate = false;  break;
                        }
                    }
                    break;
                }
            }
            if (isduplicate) {
                C_1[moshC_1] = A[i][0];
                moshC_1++;
            }
        }
        delete[] M;
        moshC = moshC_2 = 1;
    }
    break;

    case 15: //Прообраз B
    {
        int moshM;
        cout << "   Введите мощность множества М: ";    //Пользователь задает мощность области прибытия
        cin >> moshM;
        int* M = new int[moshM]; //создаем обл отправления
        cout << "      Введите элементы множества М: ";
        for (int i = 0; i < moshM; i++)
            cin >> M[i];

        for (int i = 0; i < moshB; i++) {
            bool isduplicate = false;
            for (int j = 0; j < moshM; j++) {
                if (B[i][1] == M[j]) {
                    isduplicate = true;
                    for (int k = 0; k < moshC_1; k++) {
                        if (C_1[k] == B[i][0]) {
                            isduplicate = false;  break;
                        }
                    }
                    break;
                }
            }
            if (isduplicate) {
                C_1[moshC_1] = B[i][0];
                moshC_1++;
            }
        }
        delete[] M;
        moshC = moshC_2 = 1;
    }
    break;

    case 16: //Сужение А
    {
        int moshM;
        cout << "   Введите мощность множества М: ";    //Пользователь задает мощность области отпарвления
        cin >> moshM;
        int* M = new int[moshM]; //создаем обл отправления
        cout << "      Введите элементы множества М: ";
        for (int i = 0; i < moshM; i++)
            cin >> M[i];

        for (int i = 0; i < moshA; i++) {
            bool isduplicate = false;
            for (int j = 0; j < moshM; j++) {
                if (A[i][0] == M[j]) {
                    isduplicate = true;
                    for (int k = 0; k < moshC; k++) {
                        if (C[k] == A[i]) {
                            isduplicate = false;  break;
                        }
                    }
                    break;
                }
            }
            if (isduplicate) {
                C[moshC] = A[i];
                moshC++;
            }
        }

        moshC_1 = moshM;
        for (int i = 0; i < moshM; i++)
            C_1[i] = M[i];
        C_2 = Y;
        moshC_2 = moshY;
        delete[] M;
    }
    break;

    case 17: //Сужение B
    {
        int moshM;
        cout << "   Введите мощность множества М: ";    //Пользователь задает мощность области отпарвления
        cin >> moshM;
        int* M = new int[moshM]; //создаем обл отправления
        cout << "      Введите элементы множества М: ";
        for (int i = 0; i < moshM; i++)
            cin >> M[i];

        for (int i = 0; i < moshB; i++) {
            bool isduplicate = false;
            for (int j = 0; j < moshM; j++) {
                if (B[i][0] == M[j]) {
                    isduplicate = true;
                    for (int k = 0; k < moshC; k++) {
                        if (C[k] == B[i]) {
                            isduplicate = false;  break;
                        }
                    }
                    break;
                }
            }
            if (isduplicate) {
                C[moshC] = B[i];
                moshC++;
            }
        }

        moshC_1 = moshM;
        for (int i = 0; i < moshM; i++)
            C_1[i] = M[i];
        C_2 = V;
        moshC_2 = moshV;
        delete[] M;
    }
    break;

    case 18: //продолжения А
    {
        if (moshA == (moshX * moshY))
            cout << "График полностью определен\n";
        else {
            int moshM;
            cout << "   Введите мощность графика M: ";    //Пользователь задает мощность элементы графика 
            cin >> moshM;
            int** M = new int* [moshM];
            for (int i = 0; i < moshM; i++) {
                M[i] = new int[2];
            }

            cout << "      Введите элементы графика M: ";
            for (int i = 0; i < moshM; i++) {        // Пользователь задает элементы графика 
                for (int j = 0; j < 2; j++) {
                    cin >> M[i][j];
                }
            }
            C = A;
            moshC = moshA;

            for (int i = 0; i < moshM; i++) {
                bool isduplicate = false;
                for (int j = 0; j < moshA; j++) {
                    if (A[j][0] == M[i][0] && A[j][1] == M[i][1]) {
                        isduplicate = true;  break;
                    }
                }
                if (!isduplicate) {
                    C[moshC] = M[i];
                   
                    moshC++;
                }
            }

            cout << "\nОбласть отправления: " << endl;
            for (int i = 0; i < moshX; i++) {

                cout << X[i] << " ";
            }
            cout << endl;
            cout << "Область прибытия: " << endl;
            for (int i = 0; i < moshY; i++) {

                cout << Y[i] << " ";
            }
            cout << endl;
            for (int i = 0; i < moshC; i++) {        //Вывод множества С пользователю
                cout << "<" << C[i][0] << ",";
                cout << C[i][1] << ">";
                cout << " ";
            }

            for (int i = 0; i < moshM; i++) {
                delete[] M[i];
            }
            delete[] M;
        }
    }

        break;

    case 19: //продолжения B
    {
        if (moshB == (moshX * moshY))
            cout << "График полностью определен\n";
        else {
            int moshM;
            cout << "   Введите мощность графика M: ";    //Пользователь задает мощность элементы графика 
            cin >> moshM;
            int** M = new int* [moshM];
            for (int i = 0; i < moshM; i++) {
                M[i] = new int[2];
            }

            cout << "      Введите элементы графика M: ";
            for (int i = 0; i < moshM; i++) {        // Пользователь задает элементы графика 
                for (int j = 0; j < 2; j++) {
                    cin >> M[i][j];
                }
            }
            C = B;
            moshC = moshB;

            for (int i = 0; i < moshM; i++) {
                bool isduplicate = false;
                for (int j = 0; j < moshB; j++) {
                    if (B[j][0] == M[i][0] && B[j][1] == M[i][1]) {
                        isduplicate = true;  break;
                    }
                }
                if (!isduplicate) {
                    C[moshC] = M[i];

                    moshC++;
                }
            }

            cout << "\nОбласть отправления: " << endl;
            for (int i = 0; i < moshU; i++) {

                cout << U[i] << " ";
            }
            cout << endl;
            cout << "Область прибытия: " << endl;
            for (int i = 0; i < moshV; i++) {

                cout << V[i] << " ";
            }
            cout << endl;
            for (int i = 0; i < moshC; i++) {        //Вывод множества С пользователю
                cout << "<" << C[i][0] << ",";
                cout << C[i][1] << ">";
                cout << " ";
            }

            for (int i = 0; i < moshM; i++) {
                delete[] M[i];
            }
            delete[] M;
        }
    }

    break;
    }
    if (vibor == 18 || vibor == 19)
        return 0;
    else if (moshC == 0 || moshC_1 == 0 || moshC_2 == 0) {
        cout << "C - пустое множество";
    }
    else if (vibor == 12 || vibor == 13) {
        cout << "Образ: " << endl;
        for (int i = 0; i < moshC_1; i++) {

            cout << C_1[i] << " ";
        }
    }
    else if (vibor == 14 || vibor == 15) {
        cout << "Прообраз: " << endl;
        for (int i = 0; i < moshC_1; i++) {

            cout << C_1[i] << " ";
        }
    }
    else if (vibor == 6 || vibor == 7)
    {
        cout << "Область отправления: " << endl;
        for (int i = 0; i < moshC_1; i++) {        

            cout << Ab_1[i] << " ";
        }
        cout << endl;
        cout << "Область прибытия: " << endl;
        for (int i = 0; i < moshC_2; i++) {       

            cout << Ab_2[i] << " ";
        }
        cout << endl;
        for (int i = 0; i < moshC; i++) {        //Вывод множества С пользователю
            cout << "<" << C_3[i][0] << ",";
            cout << C_3[i][1] << ">";
            cout << " ";
        }
    }
    else if (vibor == 3 )
    {
        cout << "Область отправления: " << endl;
        for (int i = 0; i < moshX; i++) {
            cout << X[i] << " ";
        }
        cout << endl;
        cout << "Область прибытия: " << endl;
        for (int i = 0; i < moshY; i++) {
            cout << Y[i] << " ";
        }
        cout << endl;
        for (int i = 0; i < moshC; i++) {        //Вывод множества С пользователю
            cout << "<" << C[i][0] << ",";
            cout << C[i][1] << ">";
            cout << " ";
        }
    }
    else if (vibor == 4)
    {
        cout << "Область отправления: " << endl;
        for (int i = 0; i < moshU; i++) {
            cout << U[i] << " ";
        }
        cout << endl;
        cout << "Область прибытия: " << endl;
        for (int i = 0; i < moshV; i++) {
            cout << V[i] << " ";
        }
        cout << endl;
        for (int i = 0; i < moshC; i++) {        //Вывод множества С пользователю
            cout << "<" << C[i][0] << ",";
            cout << C[i][1] << ">";
            cout << " ";
        }
    }
    else {
        cout << "Область отправления: " << endl;
        for (int i = 0; i < moshC_1; i++) {
            cout << C_1[i] << " ";
        }
        cout << endl;
        cout << "Область прибытия: " << endl;
        for (int i = 0; i < moshC_2; i++) {
            cout << C_2[i] << " ";
        }
        cout << endl;
        for (int i = 0; i < moshC; i++) {        //Вывод множества С пользователю
            cout << "<" << C[i][0] << ",";
            cout << C[i][1] << ">";
            cout << " ";
        }
    }

    for (int i = 0; i < moshA; i++) {
        delete[] A[i];
    }
    delete[] A;

    for (int i = 0; i < moshB; i++) {
        delete[] B[i];
    }
    delete[] B;
    for (int i = 0; i < moshA; i++) {
        delete[] D[i];
    }
    delete[] D;
    for (int i = 0; i < moshB; i++) {
        delete[] E[i];
    }
    delete[] E;

    for (int i = 0; i < 150; i++) {
        delete[] Un[i];
    }
    delete[] Un;

    delete[] X;
    delete[] Y;
    delete[] U;
    delete[] V;
    delete[] C_1;
    delete[] C_2;
    delete[] E_1;
    delete[] E_2;
    delete[] D_1;
    delete[] D_2;

    for (int i = 0; i < 100; i++) {
        delete[] C_3[i];
    }
    delete[] C_3;
    for (int i = 0; i < moshA + moshB; i++) {
        delete[] C[i];
    }
    delete[] C;
     return 0;
}