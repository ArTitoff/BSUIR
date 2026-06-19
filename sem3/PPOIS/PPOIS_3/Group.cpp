#include "Group.h"

int Group::Get_Group_ID() {
    return group_id;
}
Group::Group(int id, Department* dept, int course, string speciality) :
    group_id(id), department(dept), course(course), speciality(speciality) {
    if (department == nullptr) {
        throw invalid_argument("Указатель на кафедру не может быть null");
    }
}

void Group::Print_Department() {
    department->Print_Department();
    cout << "Курс: " << course << "  Специальность: " << speciality << endl;
}

void Group::Sort_Student() {
    for (size_t i = 0; i < students.size(); ++i) {
        for (size_t j = 0; j < students.size() - 1 - i; ++j) {
            if (students[j].Get_Name() > students[j + 1].Get_Name()) {
                swap(students[j], students[j + 1]);
            }
        }
    }
}

int Group::Get_Group_Size() {
    return students.size();
}

void Group::Display() {
    Sort_Student();
    if (!students.empty()) {
        cout << "\nСписок студентов группы: " << group_id << endl;
        for (int i = 0; i < students.size(); ++i) {
            cout << i + 1 << ". ";
            students[i].Info();
        }
    }
    else {
        cout << "В группе нет студентов." << endl;
    }
}

void Group::Display_Student_Rating(Student& student) {
    for (Subject subject : subjects)
        student.Print_Subject_Grades(subject);
    student.Print_Avarage_Sem_Grade();
}

vector<Subject> Group::Get_Subjects() {
    return subjects;
}

Student& Group::Get_Student(int i) {
    return students[i];
}

Student* Group::Get_Student_Ptr(int index) {
    return &students[index];
}

void Group::Add_Student_To_Group(Student& student) {
    students.push_back(student);
}

void Group::Add_Student_To_Group(int ID, const string& name, int age) {
    students.emplace_back(ID, name, age);
}
void Group::Delete_Student_From_Group(int index) {
    if (students.empty()) {
        cout << "Студентов и так нет\n";
        return;
    }

    students.erase(students.begin() + index);
    cout << "Студент с индексом " << index + 1 << " был удален.\n";
}


void Group::Add_Subject_To_Group(Subject& subject) {
    subjects.push_back(subject);
}