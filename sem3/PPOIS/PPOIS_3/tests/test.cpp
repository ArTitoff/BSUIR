#include "pch.h"
#include <gtest/gtest.h>
#include "../Person.h"

// Подкласс для тестирования
class TestPerson : public Person {
public:
    TestPerson(string name, int age) : Person(name, age) {};
    void Info() {
        cout << "Имя: " << name << endl;
    }
    using  Person:: ~Person;
    using  Person::Get_Name;
    using  Person::Person;
    using  Person::age;

};

class PersonTest : public ::testing::Test {
protected:
    TestPerson person; // Используем объект вместо указателя

    PersonTest() : person("Alice", 25) {} // Инициализация в конструкторе тестового класса
};

TEST_F(PersonTest, GetName) {
    EXPECT_EQ(person.Get_Name(), "Alice");
}

