#include <iostream>
#include <fstream>
#include <string>

    using namespace std;

    struct avia {
        string name;
        string type;
        int flightAltitude; 
        int maxSpeed;   //>700
        string status; //sniat s pr
    };
    avia model[30];

    void ReadFile(string& filename, int& avCol) {
        ifstream file(filename);
        if (file.is_open()) {
            while (!file.eof()) {
                string temp;
                file >> temp;
                if (temp != "") {
                    model[avCol].name = temp;
                    file >>  model[avCol].type >> model[avCol].flightAltitude >> model[avCol].maxSpeed >> temp;
                    if (temp == "в") {
                        model[avCol].status = temp;
                        file >> temp;
                        model[avCol].status = model[avCol].status + ' ' + temp;
                    }
                    else {
                        model[avCol].status = temp;
                        file >> temp;
                        model[avCol].status = model[avCol].status + ' ' + temp;
                        file >> temp;
                        model[avCol].status = model[avCol].status + ' ' + temp;
                    }
                    avCol++;
                }
            }
            file.close();
        }
        else {
            cout << "Не получилось открыть файл\n" << endl;
        }
    }

    void QuickSort(int left, int right, avia model[]) {
        if (left < right) {
            avia t;
            int i = left;
            int j = right;
            int x = model[(left + right) / 2].flightAltitude;
            while (i <= j) {
                while (model[i].flightAltitude < x)
                    i++;
                while (model[j].flightAltitude > x)
                    j--;
                if (i <= j) {
                    t = model[i];
                    model[i] = model[j];
                    model[j] = t;
                    i++;
                    j--;
                }
            }
            if (left < j)
                QuickSort(left, j, model);
            if (i < right)
                QuickSort(i, right, model);
        }
    }


void CreateNewFile(string&path) {
    ofstream file(path); 
    if (file.is_open()) {
        file.close();
        //cout << "Файл создан\n";
    }
    else cout << "Файл не создан\n";
}

void AddData(string& filename, const string& data) {
    ofstream file(filename, ios::app); 
    if (file.is_open()) {
        file << data << endl;
        file.close();
    }
    else {
        cout << "Ошибка открытия файла для записи." << endl;
    }
}

/*void AddDataForDel(string& filename, const string& data) {
    ofstream file(filename, ios::app);
    if (file.is_open()) {
        file << data << endl;
        file.close();
    }
}*/

void DeleteData(avia model[], int& avCol, int vibor, string& filename) {
    for (vibor; vibor < avCol-1; vibor++) {
        model[vibor] = model[vibor + 1];
    }
    avCol--;
    string temp;
    CreateNewFile(filename);
    for (int i = 0; i < avCol; i++) {
        temp = model[i].name + ' ' + model[i].type + ' ' + to_string(model[i].flightAltitude) + ' ' + to_string(model[i].maxSpeed) + ' ' + model[i].type;
        AddData(filename, temp);
    }
}

void LinSearch(avia model[], int& avCol, int key) {
    bool found = false;
    for (int i = 0; i < avCol; i++)
        if (model[i].flightAltitude == key) {
            found = true;
            cout << "Название: " << model[i].name << endl << "   Тип продукции:" << model[i].type << endl << "   Максимальная высота полета: " << model[i].flightAltitude << endl << "   Максимальная скорость: " << model[i].maxSpeed << endl << "   Статус: " << model[i].status << endl << endl; 
            // break; – если поле поиска уникальное
        }
    if (!found)  // Вывод сообщения, что элемент не найден 
        cout << "Элеметн не найден" << endl;
}

void BinarSearch(avia model[], int& avCol, int key) {
    int j = avCol - 1;
    int i_key = 0;
    while (i_key < j) {
       int m = (i_key + j) / 2;
        if (model[m].flightAltitude < key) i_key = m + 1;
        else j = m;
    }
    if (model[i_key].flightAltitude != key) // Элемент не найден
        cout << "Элеметн не найден" << endl;
    else 
        cout << "Название: " << model[i_key].name << endl << "   Тип продукции:" << model[i_key].type << endl << "   Максимальная высота полета: " << model[i_key].flightAltitude << endl << "   Максимальная скорость: " << model[i_key].maxSpeed << endl << "   Статус: " << model[i_key].status << endl << endl;
}

void PriamoyVibor(avia model[], int& avCol) {
    for (int i = 0; i < avCol - 1; i++) {
        int m = i;
        for (int j = i + 1; j < avCol; j++)
            if (model[j].flightAltitude < model[m].flightAltitude) m = j;
        avia a = model[m];
        model[m] = model[i];
        model[i] = a;
    }
}


void Print(avia model[], int& avCol) {
    for (int i = 0; i < avCol; i++) {
        if (model[i].maxSpeed > 700 && model[i].status == "снят с производства")
            cout << i + 1 << ". " << "Название: " << model[i].name << endl << "   Тип продукции: " << model[i].type << endl << "   Максимальная высота полета: " << model[i].flightAltitude << endl << "   Максимальная скорость: " << model[i].maxSpeed << " км/ч"  << endl << "   Статус: " << model[i].status << endl << endl;
    }
}

void PrintAllModels(avia model[], int& avCol) {
    for (int i = 0; i < avCol; i++) {  
        cout << i+1 << ". " << "Название: " << model[i].name << endl << "   Тип продукции: " << model[i].type << endl << "   Максимальная высота полета: " << model[i].flightAltitude << endl << "   Максимальная скорость: " << model[i].maxSpeed << " км/ч" << endl << "   Статус: " << model[i].status << endl << endl;
    }
}

int main() {
    string path = "Myfile.txt";
    string temp, addtemp;
    int flightAltitude, avCol, vibor;
    int choice;
    do {
        cout << "Меню:" << endl;
        cout << "1. Создать файл" << endl;
        cout << "2. Добавить данные" << endl;
        cout << "3. Просмотр всех данных файла" << endl;
        cout << "4. Удалить элемент" << endl;
        cout << "5. Линейный поиск" << endl;
        cout << "6. Бинарный поиск" << endl;
        cout << "7. Сортировка выбором" << endl;
        cout << "8. QuickSort" << endl;
        cout << "9. Вывести информацию о технике со максимальной скоростью выше 700 км/ч и имеющую статус 'снят с производства' " << endl;
        cout << "0. Выход" << endl << endl;

        cout << "Введите номер команды: ";
        cin >> choice;

        switch (choice) {
        case 1:
            CreateNewFile(path);
            cout << "Файл Myfile.txt создан" << endl;
            break;
        case 2:
            cout << "Введите название техники: " ;
            cin >> temp;
            addtemp = temp;
            cout << "Введите тип техники: ";
            cin >> temp;
            addtemp = addtemp + ' ' + temp;
            cout << "Введите максимальную высоту полета: " ;
            cin >> temp;
            addtemp = addtemp + ' ' + temp;
            cout << "Введите максимальную скорость(в км/ч) полета: ";
            cin >> temp;
            addtemp = addtemp + ' ' + temp;
            cout << "Введите статус: ";
            cin.get();
            getline(cin, temp);
            addtemp = addtemp + ' ' + temp;
            AddData(path, addtemp);
            cout << "Данные успешно добавлены " << endl;
            break;
        case 3:
            avCol = 0;
            ReadFile(path, avCol);
            if (avCol <= 0) 
                cout << "Файл пустой" << endl;
            else
                PrintAllModels(model, avCol);
            break;
        case 4:
            avCol = 0;
            ReadFile(path, avCol);
            if (avCol <= 0)
                cout << "Файл пустой" << endl;
            else {
                cout << "Выберите элемент, который хотите удалить ";
                cin >> vibor;
                if (avCol < vibor || vibor <= 0) {
                    while (avCol < vibor || vibor <= 0) {
                        cout << "Такого элемента нет. Выберите элемент, который хотите удалить ";
                        cin >> vibor;
                    }
                }
                DeleteData(model, avCol, vibor-1, path);
                cout << "Элемент " << vibor << " удален" << endl;
            }
            break;
        case 5:
            cout << "Введите высоту полета, которая вас интересует " << endl;
            cin >> flightAltitude;
            avCol = 0;
            ReadFile(path, avCol);
            if (avCol <= 0)
                cout << "Файл пустой" << endl;
            else {
                PriamoyVibor(model, avCol);
                LinSearch(model, avCol, flightAltitude);
                }
            break;
        case 6:
            cout << "Введите высоту полета, которая вас интересует " << endl;
            cin >> flightAltitude;
            avCol = 0;
            ReadFile(path, avCol);
            if (avCol <= 0)
                cout << "Файл пустой" << endl;
            else {
                PriamoyVibor(model, avCol);
                BinarSearch(model, avCol, flightAltitude);
            }
            break;
        case 7:
            cout << "Результат сортировки выбором: " << endl;
            avCol = 0;
            ReadFile(path, avCol);
            if (avCol <= 0)
                cout << "Файл пустой" << endl;
            else {
                PriamoyVibor(model, avCol);
                PrintAllModels(model, avCol);
            }
            break;
        case 8:
            cout << "Результат сортировки QuickSort: " << endl;
            avCol = 0;
            ReadFile(path, avCol);
            if (avCol <= 0)
                cout << "Файл пустой" << endl;
            else {
                QuickSort(0, avCol - 1, model);
                PrintAllModels(model, avCol);
            }
            break;
        case 9:
            avCol = 0;
            ReadFile(path, avCol);
            if (avCol <= 0)
                cout << "Файл пустой" << endl;
            else
                Print(model, avCol);
            break;
        case 0:
            cout << "Программа завершена!" << endl;
            break;
        default:
            cout << "Такого варианта нет" << endl;
        }
    } while (choice != 0);

    return 0;
}