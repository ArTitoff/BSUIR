#include "Teacher.h"

Teacher::Teacher(int ID, const string& name, int age, int experience, string job_title) :
    Person(name, age), ID(ID), experience(experience), job_title(job_title) {}

void Teacher::Add_Subject_To_Teacher(Subject& subject) {
    subjects.push_back(subject);
}

Subject& Teacher::Get_Subject() {
    for (int i = 0; i < subjects.size();i++)
        cout << i + 1 << ". " << subjects[i].Get_Subject_Name() << endl;
    cout << "Выберите номер предмета, по которую ставите оценку\n";
    int choice;
    Correct_Cin(choice, 1, subjects.size());
    return subjects[choice - 1];
}

void Teacher::Info()  {
    cout << "\nID: " << ID << " | Имя: " << name << " | Возраст: " << age << " | Должность: " << job_title << " | Опыт работы: " << experience << "\nПредметы: | ";
    for (Subject subject : subjects)
        cout << subject.Get_Subject_Name() << " | ";
}

int Teacher::Get_ID() {
    return ID;
}