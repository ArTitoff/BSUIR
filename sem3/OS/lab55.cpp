#include <iostream>
#include <cstring>
#include <vector>
#include <algorithm> 

const size_t BLOCK_SIZE = 32; 

struct Block {
    char data[BLOCK_SIZE]; 
    Block* next; 
};

struct File {
    std::string name; 
    Block* head; 
};

class FileSystem {
private:
    std::vector<File*> files;

public:
    FileSystem() {}

    // Создание файла
    File* createFile(const std::string& name) {
        File* file = new File;
        file->name = name;
        file->head = nullptr;
        files.push_back(file); 
        return file;
    }

    // Запись данных в файл
    void writeFile(File* file, const char* data) {
        size_t dataLength = strlen(data);
        size_t offset = 0;

        while (offset < dataLength) {
            Block* newBlock = new Block;

            size_t toCopy = (dataLength - offset > BLOCK_SIZE - 1) ? BLOCK_SIZE - 1 : dataLength - offset;

            strncpy(newBlock->data, data + offset, toCopy);
            newBlock->data[toCopy] = '\0'; 
            newBlock->next = nullptr;

            if (!file->head) {
                file->head = newBlock; 
            } else {
                Block* current = file->head;
                while (current->next) {
                    current = current->next; 
                }
                current->next = newBlock; // Добавить новый блок в конец
            }

            offset += toCopy; // Увеличиваем смещение
        }
    }

    // Чтение данных из файла
    void readFile(File* file) {
        Block* current = file->head;
        std::cout << "Содержимое файла \"" << file->name << "\":" << std::endl;
        while (current) {
            std::cout << current->data << std::endl;
            current = current->next;
        }
    }

void deleteFile(File* file) {
    Block* current = file->head;
    while (current) {
        Block* temp = current;
        current = current->next;
        delete temp; 
    }

    // Удаляем файл из вектора
    auto it = std::remove(files.begin(), files.end(), file);
    files.erase(it, files.end()); 
    delete file; 
}


    // Копирование файла
    File* copyFile(File* source) {
        File* newFile = createFile(source->name + "_copy"); // Создаем новый файл с "_copy" в конце
        Block* current = source->head;

        while (current) {
            writeFile(newFile, current->data); 
            current = current->next;
        }

        return newFile; // Возвращаем указатель на новый файл
    }

    // Перемещение файла
    void moveFile(File*& source, File*& destination) {
        if (destination) {
            deleteFile(destination); 
        }
        destination = copyFile(source); 
        destination->name = source->name; 
        deleteFile(source); 
        source = nullptr; 
        std::cout << "\nФайл "<< destination->name <<" перемещен\n";
    }


    // Дамп файловой системы
    void dumpFileSystem() {
        std::cout << "Структура файловой системы:" << std::endl;
        for (const auto& file : files) {
            readFile(file); // Читаем содержимое каждого файла
            std::cout << "------------------------" << std::endl;
        }
    }
};

int main() {
    FileSystem fs;

    File* file1 = fs.createFile("file1.txt");
    fs.writeFile(file1, "Hello, World! This is my file system.");
    
    fs.readFile(file1);

    File* file2 = fs.copyFile(file1);
    std::cout << "\nКопия файла создана:\n";
    
    fs.readFile(file2);

    File* file3 = nullptr;
    fs.moveFile(file1, file3);
    
      
    File* file4 = fs.createFile("file4.txt");
    fs.writeFile(file4, "There is another file4 with long-long text, that has devideted by writeFile function into blocks");

    fs.dumpFileSystem();

    fs.deleteFile(file2); 
    fs.deleteFile(file3); 
    fs.deleteFile(file4); 
    
    return 0;
}
