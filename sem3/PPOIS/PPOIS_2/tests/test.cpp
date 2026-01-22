#include "pch.h"
#include <gtest/gtest.h>
#include <sstream>
#include "../Handyman.h"
#include "../Handyman.cpp"
#include "../Author.cpp"
#include "../Person.cpp"
#include "../Workers.cpp"
#include "../Halls.cpp"
#include "../Event.cpp"
#include "../Cleaner.cpp"
#include "../Manager.cpp"
#include "../Musician.cpp"
#include "../Orchestra.cpp"
#include "../Performance.cpp"
#include "../Theater.cpp"
#include "../Visitor.cpp"
#include "../Tickets.cpp"
#include "../Actor.cpp"
#include "../Chashier.cpp"


using namespace std;

// Mock InputOutput для захвата ввода/вывода
class MockInputOutput {
public:
    std::stringstream input;
    std::stringstream output;

    MockInputOutput() {
        std::cin.rdbuf(input.rdbuf());
        std::cout.rdbuf(output.rdbuf());
    }

    ~MockInputOutput() {
        std::cin.rdbuf(nullptr);
        std::cout.rdbuf(nullptr);
        std::cout.flush();
    }
};


TEST(AuthorTest, ValidWorkInput) {
    MockInputOutput mockIO;

    
    mockIO.input << "2\n"   
        << "Работа 1\n"
        << "Работа 2\n";

    Author author({}, 50000, "01.12.2023", "Writer", 5, 1, "Bob", 30);
    author.Set_Object_Info();

   
    ASSERT_EQ(author.Get_Written_Works().size(), 2);
    EXPECT_EQ(author.Get_Written_Works()[0], "Работа 1");
    EXPECT_EQ(author.Get_Written_Works()[1], "Работа 2");
}

TEST(AuthorTest, InvalidWorkInput_NonNumeric) {
    MockInputOutput mockIO;

   
    mockIO.input << "abc\n"   
        << "2\n"     
        << "Работа 1\n"
        << "Работа 2\n";

    Author author({}, 50000, "01.12.2023", "Writer", 5, 1, "Bob", 30);
    author.Set_Object_Info();


    ASSERT_EQ(author.Get_Written_Works().size(), 2);
    EXPECT_EQ(author.Get_Written_Works()[0], "Работа 1");
    EXPECT_EQ(author.Get_Written_Works()[1], "Работа 2");
}

class TestChashier : public Chashier {
public:
    TestChashier(int salary, string hire_date, string job_title, int work_experience, int stress_level, string name, int age,
        int rows1, int cols1, int rows2, int cols2, int ticket_orch_price, int ticket_per_price) : Chashier(salary, hire_date, job_title, work_experience, stress_level, name, age,
         rows1,  cols1,  rows2,  cols2,  ticket_orch_price,  ticket_per_price) {}
    using Chashier::Check_Choice;
    using Chashier::Book_Orch;
    using Chashier::UnBook_Orch;
    using Chashier::orchestra_hall;
    using Chashier::tickets_profit;
    using Tickets::orchestra_tickets_amount;

};

TEST(AuthorTest, InvalidWorkInput_NegativeNumber) {
    MockInputOutput mockIO;

    
    mockIO.input << "-1\n"    
        << "0\n";   

    Author author({}, 50000, "01.12.2023", "Writer", 5, 1, "Bob", 30);
    author.Set_Object_Info();

    EXPECT_TRUE(author.Get_Written_Works().empty());
}

TEST(ChashierTest, CheckChoice_ValidInput) {
    MockInputOutput mockInput;
    mockInput.input << "1\n"; 

    TestChashier chashier(50000, "01.12.2023", "Cashier", 5, 1, "Bob", 30, 5, 5, 5, 5, 50, 100);

    int choice = -1; 
    chashier.Check_Choice(choice);

    EXPECT_EQ(choice, 1); 
}

TEST(ChashierTest, CheckChoice_InvalidInput_NonNumeric) {
    MockInputOutput mockInput;
    mockInput.input << "abc\n" << "2\n"; 

    TestChashier chashier(50000, "01.12.2023", "Cashier", 5, 1, "Bob", 30, 5, 5, 5, 5, 50, 100);

    int choice = -1; 
    chashier.Check_Choice(choice);

    EXPECT_EQ(choice, 2);
}

TEST(ChashierTest, CheckChoice_InvalidInput_OutOfRange) {
    MockInputOutput mockInput;
    mockInput.input << "3\n" << "1\n"; 

    TestChashier chashier(50000, "01.12.2023", "Cashier", 5, 1, "Bob", 30, 5, 5, 5, 5, 50, 100);

    int choice = -1; 
    chashier.Check_Choice(choice);

    EXPECT_EQ(choice, 1);
}


// Тест для функции Book_Orch
TEST(ChashierTest, BookOrch_Success) {
 
    MockInputOutput mockIO;

    TestChashier chashier(50000, "01.12.2023", "Cashier", 5, 1, "Bob", 30, 5, 5, 5, 5, 50, 100);

    // Имитация ввода пользователя

    mockIO.input << "1\n1\n"; // Ряд 1, место 1
    chashier.Book_Orch(); // Вызов функции
    int a = 0;
    int b = 0;
    // Проверка, что место было успешно забронировано
    EXPECT_TRUE(chashier.orchestra_hall.Get_Place_Status(a,b));
}

TEST(ChashierTest, BookOrch_AlreadyBooked) {

    MockInputOutput mockIO;

    TestChashier chashier(50000, "01.12.2023", "Cashier", 5, 1, "Bob", 30, 5, 5, 5, 5, 50, 100);

 
    mockIO.input << "1\n1\n"; // Ряд 1, место 1
    chashier.Book_Orch(); // Вызов функции

    EXPECT_EQ(chashier.orchestra_tickets_amount, 24);// Проверяем, что место теперь занято
}


TEST(ChashierTest, BookOrch_Profit) {
    MockInputOutput mockIO;

    TestChashier chashier(50000, "01.12.2023", "Cashier", 5, 1, "Bob", 30, 5, 5, 5, 5, 50, 100);


    mockIO.input << "1\n1\n";
    chashier.Book_Orch();

    EXPECT_EQ(chashier.tickets_profit, 50);
}

// Тест для функции UnBook_Orch
TEST(ChashierTest, UnBookOrch_Success) {

    MockInputOutput mockIO;

    TestChashier chashier(50000, "01.12.2023", "Cashier", 5, 1, "Bob", 30, 5, 5, 5, 5, 50, 100);

    // Имитация ввода пользователя

    mockIO.input << "1\n1\n"; // Ряд 1, место 1
    chashier.Book_Orch(); // Вызов функции
    mockIO.input << "1\n1\n"; // Ряд 1, место 1
    chashier.UnBook_Orch(); // Вызов функции
    int a = 0;
    int b = 0;
    // Проверка, что место было успешно забронировано
    EXPECT_FALSE(chashier.orchestra_hall.Get_Place_Status(a, b));
}



class TestManager : public Manager {
public:
    TestManager(string worker_of_month, int salary, string hire_date, string job_title, int work_experience,
        int stress_level, string name, int age)
        : Manager(worker_of_month, salary, hire_date, job_title, work_experience, stress_level, name, age) {}

    using Manager::Choosed_Worker;
    using Manager::Check_Work_Expirience;

};


TEST(ManagerTest, ChoosedWorker_Success) {


    Author worker1({}, 60000, "01.12.2023", "Writer", 10, 2, "Bob", 35);
    Cleaner worker2({}, 60000, "01.11.2023", "Cleaner", 10, 2, "Mark", 35);
    Chashier worker3(60000, "30.06.2023", "Chashier", 10, 2, "Lorry", 35, 5, 5, 3, 6, 12, 15);
    Handyman worker4(60000, "01.04.2023", "Handyman", 10, 2, "Hank", 35);

    TestManager manager("Лучший работник", 50000, "01.01.2020", "Менеджер", 5, 1, "Lan", 30);

    // Вызов функции Choosed_Worker с выбором 1
    const int a = 1;
    manager.Choosed_Worker(a, &worker1, &worker2, &worker3, &worker4);

    // Проверка, что работник уволен
    EXPECT_FALSE(worker1.Get_Hired_Status()); // worker1 должен быть уволен
}

//


TEST(ManagerTest, ChoosedWorker_InvalidChoice) {
    setlocale(LC_ALL, "RU");
    Author worker1({}, 60000, "01.12.2023", "Writer", 10, 2, "Bob", 35);
    Cleaner worker2({}, 60000, "01.11.2023", "Cleaner", 10, 2, "Mark", 35);
    Chashier worker3(60000, "30.06.2023", "Chashier", 10, 2, "Lorry", 35, 5, 5, 3, 6, 12, 15);
    Handyman worker4(60000, "01.04.2023", "Handyman", 10, 2, "Hank", 35);

    TestManager manager("Лучший работник", 50000, "01.01.2020", "Менеджер", 5, 1, "Lan", 30);

    // Вызов функции Choosed_Worker с выбором 1
    const int a = 5;
    testing::internal::CaptureStdout(); // Захват вывода
    manager.Choosed_Worker(a, &worker1, &worker2, &worker3, &worker4);
    string output = testing::internal::GetCapturedStdout();

    // Проверка, что вывод правильный
    EXPECT_EQ(output, ""); // Ожидаем сообщение об ошибке
}

TEST(ManagerTest, CheckWorkExperience_ValidInput) {
    MockInputOutput mockIO;
    int work_experience = 0;
    TestManager manager("Лучший работник", 50000, "01.01.2020", "Менеджер", 5, 1, "Lan", 30);

    mockIO.input << "5\n";
    manager.Check_Work_Expirience(work_experience);

    EXPECT_EQ(work_experience, 5); // Проверяем, что значение установлено правильно
}

TEST(ManagerTest, CheckWorkExperience_NonNumericInput) {
    MockInputOutput mockIO;
    int work_experience = 0;
    TestManager manager("Лучший работник", 50000, "01.01.2020", "Менеджер", 5, 1, "Lan", 30);

    mockIO.input << "asdd\n" ;

    testing::internal::CaptureStdout(); // Захват вывода
    manager.Check_Work_Expirience(work_experience);
    string output = testing::internal::GetCapturedStdout(); // Получаем захваченный вывод

    //EXPECT_EQ(work_experience, 2); // Проверяем, что значение установлено правильно
    EXPECT_EQ(output, "vbcb"); // Проверяем вывод ошибки
}






int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}