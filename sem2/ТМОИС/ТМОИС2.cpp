
#include<vector>
#include <iostream>
using namespace std;



int main()
{
    setlocale(LC_ALL, "RU");
    int vibor, moshA, moshB, moshC = 0, valE = 0, valD = 0;
    cout << "Способ задания - перечисление\n";   
    cout << "Введите мощность множества A: ";    //Пользователь задает мощность первого множества
    cin >> moshA;
    int** A = new int* [moshA];
    for (int i = 0; i < moshA; i++) {
        A[i] = new int[2];
    }
  

        cout << "Введите элементы множества A: ";
        for (int i = 0; i < moshA; i++) {        // Пользователь задает первое множество
            for (int j = 0; j < 2; j++) {
                cin >> A[i][j];
            }
        }
    

    cout << "Введите мощность множества B: ";    //Пользователь задает мощность второго множества
    cin >> moshB;
    int** B = new int* [moshA];
    for (int i = 0; i < moshB; i++) {
        B[i] = new int[2];
    }
   

        cout << "Введите элементы множества B: ";
        for (int i = 0; i < moshB; i++) {        //Пользователь задает второе множество
            for (int j = 0; j < 2; j++) {
                cin >> B[i][j];
            }
        }
    




    int x = -200;
    

    int** C = new int* [moshA + moshB];
    for (int i = 0; i < moshA + moshB; i++) {
        C[i] = new int[2];
    }
    int** D = new int* [moshA];
    for (int i = 0; i < moshA; i++) {
        D[i] = new int[2];
    }
    int** E = new int* [moshB];
    for (int i = 0; i < moshB; i++) {
        E[i] = new int[2];
    }


    int** U = new int* [150];
    for (int i = 0; i < 150; i++) {
        U[i] = new int[2];
    }

    int i = 0;
    for (int x = 1; x < 11; x++) {
        int y = 1;
        for (y; y < 11; y++) {
            U[i][0] = x;
            U[i][1] = y;
            i++;
        }
    }




    cout << "Выберите операцию над множествами:\n объединение A и B(1),\n пересечение A и B(2),\n разность A и B(3),\n разность B и A(4),\n симметрическую разность A и B(5),\n дополнение А(6),\n дополнение В(7),\n инверсия А(8),\n инверсия B(9),\n композиция А и В(10) ,\n композиция В и А(11)\n ";
    cin >> vibor;          //Выбор операции
    switch (vibor) {
    case 1:              //Объединение

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
        for (int i = 0; i < moshA; i++) {      //Берем первый элемент А
            for (int j = 0; j < moshB; j++) {    //Берем первый элемент В 
                if (A[i][0] == B[j][0] && A[i][1] == B[j][1]){
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
        for (int i = 0; i < moshA; i++) {
            C[moshC][1] = A[i][0];
            C[moshC][0] = A[i][1];
            moshC++;
        }
        break;
    case 9: //инверсия В
        for (int i = 0; i < moshB; i++) {
            C[moshC][1] = B[i][0];
            C[moshC][0] = B[i][1];
            moshC++;
        } 
        break;

    case 10:    //композиция А и В
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
        for (int i = 0; i < 100; i++) {    //Берем первый элемент U
            bool isduplicate = false;
            for (int j = 0; j < moshA; j++) {  //Берем первый элемент A 
                if (U[i][0] == A[j][0] && U[i][1] == A[j][1]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент U не равен ни одному элменту В, то записываем его в С
                C[moshC] = U[i];
                moshC++;
            }
        }                    //Берем следующий эл А
        break;

    case 7:                  //Дополнение B
        for (int i = 0; i < 100; i++) {    //Берем первый элемент U
            bool isduplicate = false;
            for (int j = 0; j < moshB; j++) {  //Берем первый элемент В 
                if (U[i][0] == B[j][0] && U[i][1] == B[j][1]) {
                    isduplicate = true;  break;
                }
            }                  //Берем следующий эл В
            if (!isduplicate) {          //Если элемент U не равен ни одному элменту В, то записываем его в С
                C[moshC] = U[i];
                moshC++;
            }
        }                    //Берем следующий эл А
        break;
        

    }
    if (moshC == 0) {
        cout << "C - пустое множество";
    }
    else {
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
    for (int i = 0; i < moshA + moshB; i++) {
        delete[] C[i];
    }
    delete[] C;
    for (int i = 0; i < 150; i++) {
        delete[] U[i];
    }
    delete[] U;
    return 0;
}