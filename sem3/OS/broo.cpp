#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <cstdlib>
#include <ctime>
#include <semaphore.h>
#include <sys/stat.h>
#include <vector>
#include <fstream>

const int BUFFER_SIZE = 10; // Размер буфера
const char* SEM_EMPTY = "/sem_empty"; // Семафор для пустых мест
const char* SEM_FULL = "/sem_full";   // Семафор для заполненных мест
const int END_SIGNAL = -1; // Специальное значение для завершения

int main() {
    srand(time(nullptr)); // Инициализация генератора случайных чисел

    // Создаем именованные семафоры
    sem_t* sem_empty = sem_open(SEM_EMPTY, O_CREAT, 0644, BUFFER_SIZE);
    sem_t* sem_full = sem_open(SEM_FULL, O_CREAT, 0644, 0);

    // Буфер для хранения чисел
    std::vector<int> buffer;
    buffer.reserve(BUFFER_SIZE); // Резервируем место в буфере

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

            int num;
            {
                // Проверяем, есть ли числа в буфере
                if (!buffer.empty()) {
                    num = buffer.back(); // Получаем последнее число
                    buffer.pop_back(); // Удаляем его из буфера
                } else {
                    num = END_SIGNAL; // Если буфер пуст, устанавливаем num в END_SIGNAL
                }
            }

            sem_post(sem_empty); // Увеличение счетчика пустых мест

            // Проверяем на END_SIGNAL
            if (num == END_SIGNAL) {
                // Если получен сигнал окончания, выходим из цикла
                break;
            }

            std::cout << "Consumed by p1: " << num << std::endl; // Выводим обработанное число
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

            int num;
            {
                // Проверяем, есть ли числа в буфере
                if (!buffer.empty()) {
                    num = buffer.back(); // Получаем последнее число
                    buffer.pop_back(); // Удаляем его из буфера
                } else {
                    num = END_SIGNAL; // Если буфер пуст, устанавливаем num в END_SIGNAL
                }
            }

            sem_post(sem_empty); // Увеличение счетчика пустых мест

            // Проверяем на END_SIGNAL
            if (num == END_SIGNAL) {
                // Если получен сигнал окончания, выходим из цикла
                break;
            }

            outfile << "Consumed by p2: " << num << std::endl; // Записываем в файл
        }
        outfile.close();
        return 0;
    }

    // Родительский процесс производитель
    std::cout << "Producer started." << std::endl;
    for (int i = 0; i < BUFFER_SIZE; ++i) {
        int num = rand() % 100 + 1; // Генерируем случайное число
        sem_wait(sem_empty); // Ожидание, пока есть место в буфере

        // Запись числа в буфер
        buffer.push_back(num); // Добавляем число в буфер

        std::cout << "Produced: " << num << std::endl;
        sem_post(sem_full); // Увеличиваем счетчик заполненных мест
        sleep(1); // Имитация времени генерации
    }

    // Сообщаем потребителям о завершении
    sem_wait(sem_empty); // Ожидание, чтобы записать конец
    buffer.push_back(END_SIGNAL); // Записываем специальное значение в буфер
    sem_post(sem_full); // Увеличиваем счетчик заполненных мест для потребителей

    // Ждем завершения дочерних процессов
    waitpid(consumer_pid1, nullptr, 0);
    waitpid(consumer_pid2, nullptr, 0);

    // Закрываем семафоры
    sem_close(sem_empty);
    sem_close(sem_full);
    sem_unlink(SEM_EMPTY);
    sem_unlink(SEM_FULL);

    std::cout << "All processes finished." << std::endl;

    return 0;
}
