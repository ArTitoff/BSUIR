#include <iostream>
#include <fstream>
#include <filesystem>

namespace fs = std::filesystem;

class FileSystem {
public:
    int createCount = 0;
    int writeCount = 0;
    int readCount = 0;
    int deleteCount = 0;
    int copyCount = 0;
    int moveCount = 0;

    void createFile(const std::string& name) {
        std::ofstream ofs(name);
        if (ofs) {
            createCount++;
            std::cout << "Файл \"" << name << "\" создан." << std::endl;
        } else {
            std::cerr << "Ошибка при создании файла \"" << name << "\"." << std::endl;
        }
    }

    void writeFile(const std::string& name, const std::string& data) {
        std::ofstream ofs(name, std::ios::app);
        if (ofs) {
            writeCount++;
            ofs << data << std::endl;
            std::cout << "Данные записаны в файл \"" << name << "\"." << std::endl;
        } else {
            std::cerr << "Ошибка при записи в файл \"" << name << "\"." << std::endl;
        }
    }

    void readFile(const std::string& name) {
        std::ifstream ifs(name);
        if (ifs) {
            readCount++;
            std::string line;
            std::cout << "Содержимое файла \"" << name << "\":" << std::endl;
            while (std::getline(ifs, line)) {
                std::cout << line << std::endl;
            }
        } else {
            std::cerr << "Файл \"" << name << "\" не найден." << std::endl;
        }
    }

    void deleteFile(const std::string& name) {
        if (fs::remove(name)) {
            deleteCount++;
            std::cout << "Файл \"" << name << "\" удален." << std::endl;
        } else {
            std::cerr << "Ошибка при удалении файла \"" << name << "\"." << std::endl;
        }
    }

    void copyFile(const std::string& source, const std::string& destination, bool overwrite = false) {
        try {
            if (fs::exists(destination) && !overwrite) {
                std::cerr << "Файл \"" << destination << "\" уже существует." << std::endl;
                return;
            }
            fs::copy(source, destination, overwrite ? fs::copy_options::overwrite_existing : fs::copy_options::none);
            copyCount++;
            std::cout << "Файл \"" << source << "\" скопирован в \"" << destination << "\"." << std::endl;
        } catch (const fs::filesystem_error& e) {
            std::cerr << "Ошибка при копировании файла: " << e.what() << std::endl;
        }
    }

    void moveFile(const std::string& source, const std::string& destination) {
        try {
            fs::rename(source, destination);
            moveCount++;
            std::cout << "Файл \"" << source << "\" перемещен в \"" << destination << "\"." << std::endl;
        } catch (const fs::filesystem_error& e) {
            std::cerr << "Ошибка при перемещении файла: " << e.what() << std::endl;
        }
    }

    void dumpFileSystem() {
        std::cout << "Содержимое текущей директории:" << std::endl;
        for (const auto& entry : fs::directory_iterator(fs::current_path())) {
            std::cout << entry.path() << std::endl;
        }
        // Вывод количества операций
        std::cout << "\nСтатистика операций:" << std::endl;
        std::cout << "Создано файлов: " << createCount << std::endl;
        std::cout << "Записей в файл: " << writeCount << std::endl;
        std::cout << "Прочитано файлов: " << readCount << std::endl;
        std::cout << "Удалено файлов: " << deleteCount << std::endl;
        std::cout << "Скопировано файлов: " << copyCount << std::endl;
        std::cout << "Перемещено файлов: " << moveCount << std::endl;
    }
};

int main() {
    FileSystem fs;

    // Примеры использования
    fs.createFile("file1.txt");
    fs.writeFile("file1.txt", "Hello, World!");
    fs.readFile("file1.txt");

    fs.createFile("file2.txt");
    fs.writeFile("file2.txt", "Text from 2 file");
    fs.copyFile("file1.txt", "file2.txt");
    fs.readFile("file2.txt");

    fs.moveFile("file2.txt", "file3.txt");
    fs.readFile("file3.txt");

    fs.deleteFile("file1.txt");
    fs.dumpFileSystem();
    return 0;
}
