#include "Site.h"

void Site::Add_Stud_Authorization(string& login, string& password, Student* student, Group* group) {
    for (int i = 0; i < authorization.size(); i++) {
        if (authorization[i].Get_Login() == login && authorization[i].Get_Password() == password) {
            cout << "Введите другой пароль\n";
            while (true) {
                cin >> password;
                if (authorization[i].Get_Password() != password)
                    break;
            }
        }
    }
    authorization.emplace_back(login, password, student, group);
}

void Site::Add_Teacher_Authorization(string& login, string& password, Teacher* teacher) {
    for (int i = 0; i < authorization.size(); i++) {
        if (authorization[i].Get_Login() == login && authorization[i].Get_Password() == password) {
            cout << "Введите другой пароль\n";
            while (true) {
                cin >> password;
                if (authorization[i].Get_Password() != password)
                    break;
            }
        }
    }
    authorization.emplace_back(login, password, teacher);
}

void Site::Remove_Student_Authorization(Student* student) {
    auto it = remove_if(authorization.begin(), authorization.end(),
        [student](const Authorization& auth) {
            return auth.Get_Student() == student; // Сравниваем указатели
        });

    if (it != authorization.end()) {
        authorization.erase(it, authorization.end()); // Удаляем найденные элементы
        cout << "Авторизация студента была удалена.\n";
    }
    else {
        cout << "Студент не найден.\n";
    }
}

void Site::Remove_Teacher_Authorization(Teacher* teacher) {
    auto it = remove_if(authorization.begin(), authorization.end(),
        [teacher](const Authorization& auth) {
            return auth.Get_Teacher() == teacher; // Сравниваем указатели
        });

    if (it != authorization.end()) {
        authorization.erase(it, authorization.end()); // Удаляем найденные элементы
        cout << "Авторизация преподавателя была удалена.\n";
    }
    else {
        cout << "Преподаватель не найден.\n";
    }
}
void Site::Add_Announcement() {
string author_id, text, date;
    cout << "Введите текст объявления\n";
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    getline(cin, text);
    cout << "Введите имя автора\n";
    getline(cin, author_id);
    while (true) {
        cout << "Введите дату объявления (DD.MM.YYYY): ";
        cin >> date;
        try {
            Correct_Date(date); // Проверка корректности даты
            break;
        }
        catch (const Data_Exception& e) {
            cout << "Ошибка: " << e.what() << endl;
        }
    }
    annoucements.emplace_back(text, author_id, date);
    cout << "Объявление добавлено\n";
}

void Site::Delete_Announcement() {
    if (annoucements.size() == 0)
        cout << "Объявлений и так нет\n";
    else {
        for (int i = 0; i < annoucements.size(); i++) {
            cout << i + 1 << ". ";
            annoucements[i].Print();
        }
        cout << "Выберите номер объявления, которое хотите удалить\n";
        int choice;
        Correct_Cin(choice, 1, annoucements.size());
        annoucements.erase(annoucements.begin() + (choice - 1));
        cout << "Объявление " << choice << " удалено." << endl;
    }
}

void Site::Timetable_Of_Group(Group& group) {
    for (Subject subject : group.Get_Subjects())
        timetable.Add_Subject_To_Timetable(subject, group);
}

void Site::Print_Site_Info() {
    cout << "\nСсылка сайта: " << site_name << "\nТелефон: " << telephone << endl;
}


void Site::Add_Department(Department& department) {
    departments.push_back(department);
}

void Site::Add_Department() {
    string name;
    cout << "Введите название кафедры\n";
    cin >> name;
    departments.emplace_back(name);
}
void Site::Delete_Department() {
    if (departments.empty()) {
        cout << "Кафедр и так нет\n";
        return;
    }
    for (int i = 0; i < departments.size(); i++) {
        cout << i + 1 << ". " << departments[i].Get_Department_Name() << endl;
    }
    cout << "Выберите номер кафедры, которую хотите удалить\n";
    int choice;
    Correct_Cin(choice, 1, departments.size());
    departments.erase(departments.begin() + (choice - 1));
    cout << "Кафедра " << choice << " удалена." << endl;
}


void Site::Add_Department(const string& name) {
    departments.emplace_back(name);
}

void Site::Add_Subject() {
    string name;
    cout << "Введите название предмета\n";
    cin >> name;
    subjects.emplace_back(name);
}

void Site::Delete_Subject() {
    if (subjects.empty()) {
        cout << "Предметов и так нет\n";
        return;
    }
    for (int i = 0; i < subjects.size(); i++) {
        cout << i + 1 << ". " << subjects[i].Get_Subject_Name() << endl;
    }
    cout << "Выберите номер предмета, которую хотите удалить\n";
    int choice;
    Correct_Cin(choice, 1, subjects.size());
    subjects.erase(subjects.begin() + (choice - 1));
    cout << "Предмет " << choice << " удален." << endl;
}

void Site::Add_Subject(Subject& subject) {
    subjects.push_back(subject);
}

void Site::Add_Teacher(Teacher& teacher) {
    teachers.push_back(teacher);
}

void Site::Delete_Teacher() {
    if (teachers.empty()) {
        cout << "Преподавателей и так нет\n";
        return;
    }
    for (int i = 0; i < teachers.size(); i++) {
        cout << i + 1 << ". " << teachers[i].Get_ID() << " " << teachers[i].Get_Name() << endl;
    }
    cout << "Выберите номер преподавателя, которого хотите убрать\n";
    int choice;
    Correct_Cin(choice, 1, teachers.size());
    Remove_Teacher_Authorization(&teachers[choice - 1]);
    teachers.erase(teachers.begin() + choice - 1);
    cout << "Преподаватель " << choice << " удален." << endl;
}

void Site::Add_Teacher() {
    if (subjects.empty()) {
        cout << "Предметов нет и так нет\n";
        return;
    }
    int  ID, age, experience;
    string name, login, password, speciality;
    cout << "Введите имя преподавателя\n";
    cin >> name;
    cout << "Введите возраст преподавателя\n";
    Correct_Cin(age, 18, 100);
    cout << "Введите ID преподавателя\n";
    Correct_Cin(ID, 100, 999);
    cout << "Введите специальность преподавателя\n";
    cin >> speciality;
    cout << "Введите стаж преподавателя\n";
    Correct_Cin(experience, 0, 100);
    teachers.emplace_back(ID, name, age, experience, speciality);

    cout << "Введите логин\n";
    cin >> login;
    cout << "Введите пароль\n";
    cin >> password;

    cout << "Ваш логин и пароль: " << login << " | " << password << endl;
    Add_Teacher_Authorization(login, password, &teachers[teachers.size() - 1]);
    for (int i = 0; i < subjects.size(); i++) {
        cout << i + 1 << ". " << subjects[i].Get_Subject_Name() << endl;
    }

    cout << "Выберите номер предмета, который хотите добавить преподавателю.\n";
    int choice_1;
    Correct_Cin(choice_1, 0, subjects.size());
    teachers[teachers.size() - 1].Add_Subject_To_Teacher(subjects[choice_1 - 1]);
}

void Site::Add_Student() {
    if (groups.empty()) {
        cout << "Групп и так нет\n";
        return;
    }
    for (int i = 0; i < groups.size(); i++) {
        cout << i + 1 << ". " << groups[i].Get_Group_ID() << endl;
    }
    cout << "Выберите номер группы, в которую хотите добавить студента\n";
    int choice, ID, age;
    string name, login, password;
    Correct_Cin(choice, 1, groups.size());
    cout << "Введите ID студента, первые 2 цифры должны совпадать с номером группы\n";
    Correct_Cin(ID, (groups[choice - 1].Get_Group_ID() / 100) * 100, (groups[choice - 1].Get_Group_ID() / 100) * 100 + 99);
    cout << "Введите имя студента\n";
    cin >> name;
    cout << "Введите возраст студента\n";
    Correct_Cin(age, 7, 100);
    groups[choice - 1].Add_Student_To_Group(ID, name, age);

    Student* newStudent = groups[choice - 1].Get_Student_Ptr(groups[choice - 1].Get_Group_Size() - 1);
    cout << "Введите логин\n";

    cin >> login;
    cout << "Введите пароль\n";
    cin >> password;

    cout << "Ваш логин и пароль: " << login << " | " << password << endl;
    Add_Stud_Authorization(login, password, newStudent, &groups[choice - 1]);

}

void Site::Delete_Student() {
    if (groups.empty()) {
        cout << "Групп и так нет\n";
        return;
    }
    for (int i = 0; i < groups.size(); i++) {
        cout << i + 1 << ". " << groups[i].Get_Group_ID() << endl;
    }
    cout << "Выберите номер группы, в которой хотите убрать студента\n";
    int choice;
    Correct_Cin(choice, 1, groups.size());
    groups[choice - 1].Display();
    cout << "Выберите номер , чтобы убрать студента\n";
    int index;
    Correct_Cin(index, 1, groups[choice - 1].Get_Group_Size());
    Remove_Student_Authorization(groups[choice - 1].Get_Student_Ptr(index - 1));
    groups[choice - 1].Delete_Student_From_Group(index - 1);
}

void Site::Add_Group() {
    int group_id;
    int course;
    string speciality;
    if (subjects.empty()) {
        cout << "Предметов и так нет\n";
        return;
    }
    cout << "Введите номер группы (от 1000 до 9000)\n";
    Correct_Cin(group_id, 1000, 9000);
    cout << "Введите курс (от 1 до 4)\n";
    Correct_Cin(course, 1, 4);
    cout << "Введите специальность\n";
    cin >> speciality;
    if (departments.size() != 0) {
        int index_dep;
        for (int j = 0; j < departments.size(); j++)
            cout << j + 1 << ". " << departments[j].Get_Department_Name() << endl;
        cout << "\nВыберите номер кафедры, которую хотите добавить для группы\n";
        Correct_Cin(index_dep, 1, departments.size());

        groups.emplace_back(group_id, &departments[index_dep - 1], course, speciality);
        cout << "Создана группа: " << group_id << endl;
        for (int i = 0; i < subjects.size(); i++) {
            cout << i + 1 << ". " << subjects[i].Get_Subject_Name() << endl;
        }

        while (true) {
            cout << "Выберите номер предмета, который хотите добавить группе. Для вызода нажмите 0\n";
            int choice_1;
            Correct_Cin(choice_1, 0, subjects.size());
            if (choice_1 == 0)
                break;
            groups[groups.size() - 1].Add_Subject_To_Group(subjects[choice_1 - 1]);
            cout << "Добавлен предмет " << subjects[choice_1 - 1].Get_Subject_Name() << endl;
        }
        Timetable_Of_Group(groups[groups.size() - 1]);
    }
    else cout << "Нужно создать кафедру " << endl;
}

void Site::Delete_Group() {
    if (groups.size() == 0)
        cout << "Групп и так нет\n";
    else {
        for (int i = 0; i < groups.size(); i++) {
            cout << i + 1 << ". " << groups[i].Get_Group_ID() << endl;
        }
        cout << "Выберите номер группы, которую хотите удалить\n";
        int choice;
        Correct_Cin(choice, 1, groups.size());
        for (int j = 0; j < groups[choice - 1].Get_Group_Size();j++)
            Remove_Student_Authorization(groups[choice - 1].Get_Student_Ptr(j));
        groups.erase(groups.begin() + (choice - 1));
        cout << "Группа " << choice << " удалена." << endl;
    }
}

void Site::Add_Group(Group& group) {
    groups.push_back(group);
}

void Site::Add_Pre_Stud_To_Group(Group& group, Student& stud) {
    group.Add_Student_To_Group(stud);
}

void Site::Teacher_Menu(Teacher& teacher) {
    int choice;
    do {
        cout << "1. Профиль" << endl;
        cout << "2. Выбрать группу, которой нужно поставить пропуски" << endl;
        cout << "3. Выбрать группу, которой нужно убрать пропуски" << endl;
        cout << "4. Поставить оценку" << endl;
        cout << "5. Убрать оценку" << endl;
        cout << "6. Информация о сайте" << endl;
        cout << "7. Выход" << endl;
        Correct_Cin(choice, 1, 7);
        cout << endl;
        Choosed_Menu_Teacher(choice, teacher);
        cout << endl;
    } while (choice != 7);
}

void Site::Get_Group_Num(int& choice) {
    for (int i = 0; i < groups.size();i++)
        cout << i + 1 << ". " << groups[i].Get_Group_ID() << endl;
    cout << "Выберите номер группы, которую хотите отметить\n";
    Correct_Cin(choice, 1, groups.size());
    groups[choice - 1].Display();
}

void Site::Choosed_Menu_Teacher(const int& choice, Teacher& teacher) {
    switch (choice) {
    case 1:
        teacher.Info();
        break;
    case 2:
        int choice;
        Get_Group_Num(choice);
        int choice_2;
        while (true) {
            cout << "Выберите номер студента, которого хотите отметить. Чтобы выйти, нажмите 0\n";
            Correct_Cin(choice_2, 0, groups[choice - 1].Get_Group_Size());
            if (choice_2 == 0)
                break;
            absence.Add_Absence(groups[choice - 1].Get_Student(choice_2 - 1));
        }
        break;
    case 3:
        Get_Group_Num(choice);
        while (true) {
            cout << "Выберите номер студента, у которого хотите убрать пропуск. Чтобы выйти, нажмите 0\n";
            Correct_Cin(choice_2, 0, groups[choice - 1].Get_Group_Size());
            if (choice_2 == 0)
                break;
            absence.Delete_Absence(groups[choice - 1].Get_Student(choice_2 - 1));
        }
        break;
    case 4:
        Get_Group_Num(choice);
        while (true) {
            cout << "Выберите номер студента, которому хотите поставить оценку. Чтобы выйти, нажмите 0\n";
            Correct_Cin(choice_2, 0, groups[choice - 1].Get_Group_Size());
            if (choice_2 == 0)
                break;
            int grade;
            cout << "Введите оценку, которую хотите поставить (1-10):\n";
            Correct_Cin(grade, 1, 10);
            Student& student = groups[choice - 1].Get_Student(choice_2 - 1);
            student.Add_Grade(teacher.Get_Subject(), grade);
        }
        break;
    case 5:
        Get_Group_Num(choice);
        while (true) {
            cout << "Выберите номер студента, которому хотите убрать оценку. Чтобы выйти, нажмите 0\n";
            Correct_Cin(choice_2, 0, groups[choice - 1].Get_Group_Size());
            if (choice_2 == 0)
                break;
            int grade;
            cout << "Введите оценку, которую хотите убрать (1-10):\n";
            Correct_Cin(grade, 1, 10);
            Student& student = groups[choice - 1].Get_Student(choice_2 - 1);
            student.Delete_Grade(teacher.Get_Subject(), grade);
        }
        break;
    case 6:
        Print_Site_Info();
        break;
    case 7:
        cout << "Хорошего дня!\n";
        break;
    default:
        cout << "Такого варианта нет" << endl;
    }
}

void Site::Student_Menu(Student& student, Group& group) {
    int choice;
    do {
        cout << "1. Профиль" << endl;
        cout << "2. Рейтинг" << endl;
        cout << "3. Пропуски" << endl;
        cout << "4. Спиок группы" << endl;
        cout << "5. Расписание" << endl;
        cout << "6. Преподаватели" << endl;
        cout << "7. Объявления" << endl;
        cout << "8. Информация о сайте" << endl;
        cout << "9. Выход" << endl;
        Correct_Cin(choice, 1, 9);
        cout << endl;
        Choosed_Menu_Student(choice, student, group);
        cout << endl;
    } while (choice != 9);
}

void Site::Choosed_Menu_Student(const int& choice, Student& student, Group& group) {
    switch (choice) {
    case 1:
        student.Info();
        group.Print_Department();
        cout << "Средний балл за семестр: " << student.Print_Avarage_Sem_Grade() << endl;
        salary.Student_Salary(student.Print_Avarage_Sem_Grade());
        break;
    case 2:
        group.Display_Student_Rating(student);
        break;
    case 3:
        absence.Print_Absences(student);
        break;
    case 4:
        group.Display();
        break;
    case 5:
        timetable.Print_Time_Table(group);
        break;
    case 6:
        for (Teacher teacher : teachers)
            teacher.Info();
        break;
    case 7:
        for (Announcement annoucement : annoucements)
            annoucement.Print();
        break;
    case 8:
        Print_Site_Info();
        break;
    case 9:
        cout << "Хорошего дня!\n";
        break;
    default:
        cout << "Такого варианта нет" << endl;
    }
}

void Site::Admin_Menu() {
    int choice;
    do {
        cout << "1. Добавить объявление" << endl;
        cout << "2. Убрать объявление" << endl;
        cout << "3. Добавить группу" << endl;
        cout << "4. Убрать группу" << endl;
        cout << "5. Добавить студента" << endl;
        cout << "6. Убрать студента" << endl;
        cout << "7. Добавить кафедру" << endl;
        cout << "8. Убрать кафедру" << endl;
        cout << "9. Добавить преподавателя" << endl;
        cout << "10. Убрать преподавателя" << endl;
        cout << "11. Добавить предмет" << endl;
        cout << "12. Убрать предмет" << endl;
        cout << "13. Выход" << endl;
        Correct_Cin(choice, 1, 13);
        cout << endl;
        Choosed_Menu_Admin(choice);
        cout << endl;
    } while (choice != 13);
}

void Site::Choosed_Menu_Admin(const int& choice) {
    switch (choice) {
    case 1:
        Add_Announcement();
        break;
    case 2:
        Delete_Announcement();
        break;
    case 3:
        Add_Group();
        break;
    case 4:
        Delete_Group();
        break;
    case 5:
        Add_Student();
        break;
    case 6:
        Delete_Student();
        break;
    case 7:
        Add_Department();
        break;
    case 8:
        Delete_Department();
        break;
    case 9:
        Add_Teacher();
        break;
    case 10:
        Delete_Teacher();
        break;
    case 11:
        Add_Subject();
        break;
    case 12:
        Delete_Subject();
        break;
    case 13:
        cout << "Хорошего дня!\n";
        break;
    default:
        cout << "Такого варианта нет" << endl;
    }
}

void Site::Main_Menu() {
    int choice;
    do {
        cout << "1. Войти как Студент" << endl;
        cout << "2. Войти как Учитель" << endl;
        cout << "3. Войти как Суперадмин" << endl;
        cout << "4. Выход" << endl;
        Correct_Cin(choice, 1, 4);
        cout << endl;
        Choosed_Main_Menu(choice);
        cout << endl;
    } while (choice != 4);
}

void Site::Choosed_Main_Menu(const int& choice) {
    string login, password;
    switch (choice) {
    case 1:
        cout << "Введите логин: ";
        cin >> login;
        cout << "Введите пароль: ";
        cin >> password;
        for (int i = 0; i < authorization.size(); i++) {
            if (authorization[i].Get_Login() == login && authorization[i].Get_Password() == password) {
                Student* studentPtr = authorization[i].Get_Student();
                Group* groupPtr = authorization[i].Get_Group_For_Menu();

                if (studentPtr != nullptr && groupPtr != nullptr) {
                    Student_Menu(*studentPtr, *groupPtr); // Разыменовываем указатели
                }
                else {
                    cout << "Ошибка: Студент или группа не найдены." << endl;
                }
                return; // Завершаем выполнение после успешной аутентификации
            }
        }
        cout << "Неверный логин или пароль." << endl;
        break;
    case 2:
        cout << "Введите логин: ";
        cin >> login;
        cout << "Введите пароль: ";
        cin >> password;
        for (int i = 0; i < authorization.size(); i++) {
            if (authorization[i].Get_Login() == login && authorization[i].Get_Password() == password) {
                Teacher* teacher = authorization[i].Get_Teacher();

                if (teacher != nullptr) {
                    Teacher_Menu(*teacher); // Разыменовываем указатели
                }
                else {
                    cout << "Ошибка: Преподаватель не найден." << endl;
                }
                return; // Завершаем выполнение после успешной аутентификации
            }
        }
        cout << "Неверный логин или пароль." << endl;
        break;
    case 3:
        Admin_Menu();
        break;
    case 4:
        cout << "Хорошего дня!\n";
        break;
    default:
        cout << "Такого варианта нет" << endl;
    }
}

const string Site::site_name = "http:/site.iss.com";
const string Site::telephone = "+1234567";