#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lab44.h"

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

            file->index_of_memory -= (current->length + 5);

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
