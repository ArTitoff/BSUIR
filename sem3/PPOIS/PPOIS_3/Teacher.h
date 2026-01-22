#pragma once
#include "Person.h"
#include "Subject.h"

class Teacher : public Person {
protected:
    int ID;
    string job_title;
    int experience;
    vector<Subject> subjects;

public:
    Teacher(int ID, const string& name, int age, int experience, string job_title);

    void Add_Subject_To_Teacher(Subject& subject);

    Subject& Get_Subject();

    void Info() override;

    int Get_ID();
};
