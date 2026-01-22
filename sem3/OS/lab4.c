#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct block {
    char idtf[5];
    int length;
    int have_data;
    int data_length;
    struct block* next;
};

struct FileManager {
    int index_of_memory;
    int data_index;
    char data[100];
    struct block* head;
};

void compactData(struct FileManager* file) {
    int writeIndex = 0;
    const int dataSize = sizeof(file->data) / sizeof(file->data[0]);

    for (int i = 0; i < dataSize; i++) {
        if (file->data[i] != '0') {
            file->data[writeIndex++] = file->data[i];
        }
    }

    for (int i = writeIndex; i < dataSize; i++) {
        file->data[i] = '\0';
    }

    struct block* temp = file->head;

    while (temp != NULL) {
        if (temp->have_data)
            temp->length = temp->data_length;
        temp = temp->next;
    }
    file->index_of_memory = writeIndex;
}

void Add_Block(struct FileManager* file, int length, const char id[5]) {
    if (100 - file->index_of_memory < length + 5) {
        printf("Нет столько памяти для выделения\n");
        return;
    }

    struct block* ptr = (struct block*)malloc(sizeof(struct block));
    ptr->length = length;
    ptr->next = file->head;
    file->head = ptr;

    for (int i = 0; i < 5; i++) {
        ptr->idtf[i] = id[i];
    }

    file->index_of_memory += (length + 5);
}

void view(struct block* t) {
    while (t != NULL) {
        printf("Length: %d, ID: ", t->length);
        for (int i = 0; i < 5; i++) {
            printf("%c", t->idtf[i]);
        }
        printf("\n");
        t = t->next;
    }
}

void Write_Data(struct FileManager* file, const char write_data[], const char id[5]) {
    file->data_index = 0;
    int is_block = 0;
    struct block* temp = file->head;

    while (temp != NULL) {
        is_block = (strncmp(id, temp->idtf, 5) == 0);

        if (is_block) {
            if (temp->length < strlen(write_data)) {
                printf("Не хватит памяти, чтобы записать ваши данные в этот блок\n");
                return;
            }

            temp->data_length = strlen(write_data);
            temp->have_data = 1;

            for (int i = file->data_index; i < file->data_index + temp->length + 5; i++) {
                file->data[i] = '0';
            }

            for (int i = 0; i < 5; i++) {
                file->data[file->data_index + i] = temp->idtf[i];
            }

            file->data_index += 5;

            for (int i = 0; i < strlen(write_data); i++) {
                file->data[file->data_index + i] = write_data[i];
            }

            break;
        }

        file->data_index += temp->length + 5;
        temp = temp->next;
    }
}

void Read_Data(struct FileManager* file, const char id[5]) {
    file->data_index = 0;
    int is_block = 0;
    struct block* temp = file->head;

    while (temp != NULL) {
        is_block = (strncmp(id, temp->idtf, 5) == 0);

        if (is_block) {
            if (!temp->have_data) {
                printf("Данных в блоке нет\n");
                return;
            }
            for (int i = file->data_index; i < file->data_index + temp->length + 5; i++) {
                printf("%c", file->data[i]);
            }
            printf("\n");
            break;
        }

        file->data_index += (temp->length + 5);
        temp = temp->next;
    }
}

void Del_Block(struct FileManager* file, struct block** top, const char id[5]) {
    file->data_index = 0;
    struct block* temp = NULL;
    struct block* current = *top;

    while (current != NULL) {
        int is_block = (strncmp(id, current->idtf, 5) == 0);

        if (is_block) {
            for (int i = file->data_index; i < file->data_index + current->length + 5; i++) {
                file->data[i] = '0';
            }

	    file->index_of_memory -= (current->length +5);

            if (current == *top) {
                *top = current->next;
            } else {
                temp->next = current->next;
            }

            free(current);
            break;
        }

        file->data_index += current->length + 5;
        temp = current;
        current = current->next;
    }
}

void del(struct block** top) {
    if (top == NULL || *top == NULL) {
        return;
    }

    struct block* t;

    while (*top != NULL) {
        t = *top;
        *top = (*top)->next;
        free(t);
    }
}

int main() {
    struct FileManager file;
    file.index_of_memory = 0;
    file.data_index = 0;
    memset(file.data, 0, sizeof(file.data));
    file.head = NULL;

    char ind1[5] = { 'A', 'B', 'C', 'D', '1' };
    char ind2[5] = { 'A', 'B', 'C', 'D', '2' };
    char ind3[5] = { 'A', 'B', 'C', 'D', '3' };
    char ind4[5] = { 'A', 'B', 'C', 'D', '4' };
    char ind5[5] = { 'A', 'B', 'C', 'D', '5' };
    char ind6[5] = { 'A', 'B', 'C', 'D', '6' };
    char ind7[5] = { 'A', 'B', 'C', 'D', '7' };

    Add_Block(&file, 1, ind1);
    Add_Block(&file, 5, ind2);
    Add_Block(&file, 7, ind3);
    Add_Block(&file, 4, ind4);
    Add_Block(&file, 10, ind5);
    Add_Block(&file, 10, ind6);
    Add_Block(&file, 90, ind7);

    printf("Содержимое списка:\n");
    view(file.head);

    printf("Значения data: ");
    for (int i = 0; i < 100; i++) {
        printf("%c", file.data[i]);
    }
    printf("\n");

    const char write_1[] = "Olaaa";
    Write_Data(&file, write_1, ind2);

    const char write_2[] = "BlaBla";
    Write_Data(&file, write_2, ind1);

    printf("Данные после записи:\n");
    Read_Data(&file, ind2);

    const char write_data[] = "Hello";
    Write_Data(&file, write_data, ind3);

    printf("Данные после записи:\n");
    Read_Data(&file, ind3);

    const char write_6[] = "Privet";
    Write_Data(&file, write_6, ind6);

    printf("Данные после записи:\n");
    Read_Data(&file, ind6);

    printf("Данные перед удаления блока:\n");
    for (int i = 0; i < 100; i++) {
        printf("%c", file.data[i]);
    }
    printf("\n\n");

    Del_Block(&file, &file.head, ind3);

    printf("Данные после удаления блока:\n");
    for (int i = 0; i < 100; i++) {
        printf("%c", file.data[i]);
    }
    printf("\n\n");

    compactData(&file);

    printf("Данные после операции перемещения:\n");
    for (int i = 0; i < 100; i++) {
        printf("%c", file.data[i]);
    }
    printf("\n\n");

    const char write_5[] = "Poka";
    Write_Data(&file, write_5, ind5);

    printf("Данные после записи:\n");
    Read_Data(&file, ind5);

    printf("Данные перед удаления блока:\n");
    for (int i = 0; i < 100; i++) {
        printf("%c", file.data[i]);
    }
    printf("\n\n");

    view(file.head);

    Read_Data(&file, ind6);
    del(&file.head);
    printf("После очистки:\n");
    view(file.head);

    return 0;
}
