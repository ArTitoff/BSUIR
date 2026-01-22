#include <iostream>
#include <cstring>
using namespace std;

struct block {
    char idtf[5];
    int length = 0;
    bool have_data = false;
    int data_length = 0;
    block* next;
};

struct FileManager {
    int index_of_memory = 0;
    int data_index = 0;
    char data[100] = { 0 };
    block* head = nullptr;
};

void compactData(FileManager& file) {
    int writeIndex = 0;
    const int dataSize = sizeof(file.data) / sizeof(file.data[0]);

    for (int i = 0; i < dataSize; i++) {
        if (file.data[i] != '0') {
            file.data[writeIndex++] = file.data[i];
        }
    }

    for (int i = writeIndex; i < dataSize; i++) {
        file.data[i] = '\0';
    }

    block* temp = file.head;

    while (temp != nullptr) {
        if (temp->have_data)
            temp->length = temp->data_length;
        temp = temp->next;
    }
}

void Add_Block(FileManager& file, int length, const char id[5]) {
    if (100 - file.index_of_memory < length + 5) {
        cout << "Нет столько памяти для выделения" << endl;
        return ;
    }

    block* ptr = new block;
    ptr->length = length;
    ptr->next = file.head;
    file.head = ptr;

    for (int i = 0; i < 5; i++) {
        ptr->idtf[i] = id[i];
    }

    file.index_of_memory += (length + 5);

}

void view(block* t) {
    while (t != nullptr) {
        cout << "Length: " << t->length << ", ID: ";
        for (int i = 0; i < 5; i++)
        cout << t->idtf[i] ;
        cout << endl;
        t = t->next;
    }
}

void Write_Data(FileManager& file, const char write_data[], const char id[5]) {
    file.data_index = 0;
    bool is_block = false;
    block* temp = file.head;

    while (temp != nullptr) {
        is_block = (strncmp(id, temp->idtf, 5) == 0);

        if (is_block) {
            if (temp->length < strlen(write_data)) {
                cout << "Не хватит памяти, чтобы записать ваши данные в этот блок\n";
                return;
            }

            temp->data_length = strlen(write_data); // Изменяем значение data_length
            temp->have_data = true;

            for (int i = file.data_index; i < file.data_index + temp->length + 5; i++) {
                file.data[i] = '0';
            }

            for (int i = 0; i < 5; i++) {
                file.data[file.data_index + i] = temp->idtf[i];
            }

            file.data_index += 5;

            for (int i = 0; i < strlen(write_data); i++) {
                file.data[file.data_index + i] = write_data[i];
            }

            break;
        }

        file.data_index += temp->length + 5;
        temp = temp->next;
    }
}

void Read_Data(FileManager& file, const char id[5]) {
    file.data_index = 0;
    bool is_block = false;
    block* temp = file.head;

    while (temp != nullptr) {
        is_block = (strncmp(id, temp->idtf, 5) == 0);

        if (is_block) {
            if (!temp->have_data) {
                cout << "Данных в блоке нет";
                return;
            }
            for (int i = file.data_index; i < file.data_index + temp->length + 5; i++) {
                cout << file.data[i];
            }
            cout << endl;
            break;
        }

        file.data_index += (temp->length + 5);
        temp = temp->next;

    }
}

void Del_Block(FileManager& file, block** top, const char id[5]) {
    file.data_index = 0;
    block* temp = nullptr;
    block* current = *top;

    while (current != nullptr) {
        bool is_block = (strncmp(id, current->idtf, 5) == 0);

        if (is_block) {
            for (int i = file.data_index; i < file.data_index + current->length + 5; i++) {
                file.data[i] = '0';
            }

            if (current == *top) {
                *top = current->next;
            }
            else {
                temp->next = current->next;
            }

            delete current;
            break;
        }

        file.data_index += current->length + 5;
        temp = current;
        current = current->next;
    }
}

void del(block** top) {
    if (top == nullptr || *top == nullptr) {
        return;
    }

    block* t;

    while (*top != nullptr) {
        t = *top;
        *top = (*top)->next;
        delete t;
    }
}

int main() {
    setlocale(LC_ALL, "RU");
    FileManager file;
    char ind1[5] = { 'A', 'B', 'C', 'D', '1' };
    char ind2[5] = { 'A', 'B', 'C', 'D', '2' };
    char ind3[5] = { 'A', 'B', 'C', 'D', '3' };
    char ind4[5] = { 'A', 'B', 'C', 'D', '4' };
    char ind5[5] = { 'A', 'B', 'C', 'D', '5' };
    char ind6[5] = { 'A', 'B', 'C', 'D', '6' };
    char ind7[5] = { 'A', 'B', 'C', 'D', '7' };

    Add_Block(file,  1, ind1);
    Add_Block(file,  5, ind2);
    Add_Block(file,  7, ind3);
    Add_Block(file,  4, ind4);
    Add_Block(file,  10, ind5);
    Add_Block(file,  10, ind6);
    Add_Block(file,  90, ind7);

    cout << "Содержимое списка:" << endl;
    view(file.head);

    for (int i = 0; i < 100; i++) {
        file.data[i] = 0;
    }

    cout << "Значения data: ";
    for (int i = 0; i < 100; i++) {
        cout << file.data[i];
    }
    cout << endl;

    const char write_1[] = "Olaaa";
    Write_Data(file, write_1, ind2);

    const char write_2[] = "BlaBla";
    Write_Data(file, write_2, ind1);

    cout << "Данные после записи:" << endl;
    Read_Data(file, ind2);

    const char write_data[] = "Hello";
    Write_Data(file, write_data, ind3);

    cout << "Данные после записи:" << endl;
    Read_Data(file,  ind3);

    const char write_6[] = "Privet";
    Write_Data(file, write_6, ind6);

    cout << "Данные после записи:" << endl;
    Read_Data(file,  ind6);

    cout << "Данные перед удаления блока:" << endl;
    for (int i = 0; i < 100; i++) {
        cout << file.data[i];
    }
    cout << endl << endl;

    Del_Block(file, &file.head, ind3);

    cout << "Данные после удаления блока:" << endl;
    for (int i = 0; i < 100; i++) {
        cout << file.data[i];
    }
    cout << endl << endl;

    compactData(file);

    cout << "Данные после операции перемещения:" << endl;
    for (int i = 0; i < 100; i++) {
        cout << file.data[i];
    }
    cout << endl << endl;

    const char write_5[] = "Poka";
    Write_Data(file, write_5, ind5);

    cout << "Данные после записи:" << endl;
    Read_Data(file, ind5);

    cout << "Данные перед удаления блока:" << endl;
    for (int i = 0; i < 100; i++) {
        cout << file.data[i];
    }
    cout << endl << endl;

    view(file.head);

    Read_Data(file, ind6);

    del(&file.head);
    cout << "После очистки:" << endl;
    view(file.head);

    return 0;
}