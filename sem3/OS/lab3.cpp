#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <cstdlib>
#include <ctime>
#include <semaphore.h>
#include <sys/stat.h>
#include <fstream>
#include <string>
#include <vector>

const int BUFFER_SIZE = 10; // Размер буфера
const char* SEM_EMPTY = "/sem_empty"; // Семафор для пустых мест
const char* SEM_FULL = "/sem_full";   // Семафор для заполненных мест
const char* FILENAME = "buffer.txt";   // Имя файла для хранения данных
const int END_SIGNAL = -1;


void removeLine(const std::string& filename, int lineToRemove) {
    std::ifstream inputFile(filename);
    std::vector<std::string> lines;

    // Читаем все строки из файла
    std::string line;
    int lineNumber = 0;
    while (std::getline(inputFile, line)) {
        if (lineNumber != lineToRemove) {
            lines.push_back(line); // Добавляем строки, которые не нужно удалять
        }
        lineNumber++;
    }
    inputFile.close();

    // Записываем обратно в файл все строки, кроме удаляемой
    std::ofstream outputFile(filename);
    for (const auto& l : lines) {
        outputFile << l << std::endl;
    }
    outputFile.close();
}

int main() {
    srand(time(nullptr)); // Инициализация генератора случайных чисел

    // Создаем именованные семафоры
    sem_t* sem_empty = sem_open(SEM_EMPTY, O_CREAT, 0644, BUFFER_SIZE);
    sem_t* sem_full = sem_open(SEM_FULL, O_CREAT, 0644, 0);

    // Создаем дочерний процесс для консумирования в консоль
    pid_t consumer_pid1 = fork();
    if (consumer_pid1 < 0) {
        perror("fork");
        return 1;
    }

    if (consumer_pid1 == 0) { // Дочерний процесс 1
        std::cout << "Consumer 1 started." << std::endl;
        while (true) {
            sem_wait(sem_full); // Ожидание заполненных мест

            // Чтение числа из файла
            std::ifstream infile(FILENAME);
            int num;
            infile >> num;
            infile.close();
            if(num == END_SIGNAL){
                sem_post(sem_full);
                break;

            }

            // Удаляем число из файла
            std::ofstream outfile(FILENAME);
            removeLine(FILENAME,0);
            outfile.close();
            sem_post(sem_empty); // Увеличение счетчика пустых мест
            std::cout << "Consumed by p1: " << num << std::endl;
        }
        return 0;
    }


    // Создаем дочерний процесс для консумирования в файл
    pid_t consumer_pid2 = fork();
    if (consumer_pid2 < 0) {
        perror("fork");
        return 1;
    }

    if (consumer_pid2 == 0) { // Дочерний процесс 2
        std::ofstream outfile("output.txt", std::ios::app);
        if (!outfile) {
            std::cerr << "Error opening file!" << std::endl;
            return 1;
        }

        std::cout << "Consumer 2 started." << std::endl;
        while (true) {
            sem_wait(sem_full); // Ожидание заполненных мест

            // Чтение числа из файла
            std::ifstream infile(FILENAME);
            int num;
            infile >> num;
            infile.close();

            if(num == END_SIGNAL){
                sem_post(sem_full);
                break;

            }

            // Удаляем число из файла
            std::ofstream temp_out(FILENAME);
            removeLine(FILENAME,0);
            temp_out.close();

            sem_post(sem_empty); // Увеличение счетчика пустых мест
            outfile << "Consumed by p2: " << num << std::endl;

        }
        outfile.close();
        return 0;
    }

    // Родительский процесс производитель
    std::cout << "Producer started." << std::endl;
    for (int i = 0; i < BUFFER_SIZE+1; ++i) {
        if(i == BUFFER_SIZE){
            sem_wait(sem_empty); // Убедимся, что есть место для завершения
            std::ofstream outfile(FILENAME, std::ios::app);
            outfile << END_SIGNAL << std::endl; // Записываем специальное значение
            outfile.close();
            sem_post(sem_full); // Увеличиваем счетчик заполненных мест


        }
        else{
        int num = rand() % 100 + 1; // Генерируем случайное число
        sem_wait(sem_empty); // Ожидание, пока есть место в буфере

        // Запись числа в файл
        std::ofstream outfile(FILENAME, std::ios::app);
        outfile << num << std::endl;
        outfile.close();

        std::cout << "Produced: " << num << std::endl;
        sem_post(sem_full); // Увеличиваем счетчик заполненных мест
        sleep(1); // Имитация времени генерации
    }
    }


    // Ждем завершения дочерних процессов
    waitpid(consumer_pid1, nullptr, 0);
    waitpid(consumer_pid2, nullptr, 0);

    // Закрываем семафоры
    sem_close(sem_empty);
    sem_close(sem_full);
    sem_unlink(SEM_EMPTY);
    sem_unlink(SEM_FULL);

    std::cout << "All processes finished." << std::endl;
    removeLine(FILENAME,0);

    return 0;
}

