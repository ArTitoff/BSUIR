#include <gtest/gtest.h>
#include "Site.h"
#include <iostream>


using namespace std;

class TestPerson : public Person {
public:
    TestPerson(string name, int age) : Person(name, age) {}

    void Info() override {
        cout << "Name: " << name << endl;  
    }
};

class PersonTest : public ::testing::Test {
protected:
    TestPerson person; 

    PersonTest() : person("Alice", 25) {}
};


TEST_F(PersonTest, GetName) {
    EXPECT_EQ(person.Get_Name(), "Alice");
}

TEST(SubjectTest, GetSubjectName) {
    Subject subject("Math");
    EXPECT_EQ(subject.Get_Subject_Name(), "Math");
}
class StudentTest : public ::testing::Test {
protected:
    Student* student;
    Subject subject;

    StudentTest() : student(new Student(1, "Alice", 25)), subject("Math") {}

    ~StudentTest() {
        delete student;
    }
};

TEST_F(StudentTest, GetID) {
    EXPECT_EQ(student->Get_ID(), 1);
}

TEST_F(StudentTest, AddGrade) {
    student->Add_Grade(subject, 9);
    student->Add_Grade(subject, 8);

    EXPECT_EQ(student->Print_Avarage_Sem_Grade(), (9 + 8) / 2.0);
}

TEST_F(StudentTest, DeleteGrade) {
    student->Add_Grade(subject, 9);
    student->Add_Grade(subject, 8);

    student->Delete_Grade(subject, 9);

    EXPECT_EQ(student->Print_Avarage_Sem_Grade(), 8); 
}

TEST_F(StudentTest, PrintSubjectGrades) {
    student->Add_Grade(subject, 9);
    student->Add_Grade(subject, 8);

    testing::internal::CaptureStdout(); 
    student->Print_Subject_Grades(subject);
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("Math") != std::string::npos);
    EXPECT_TRUE(output.find("9") != std::string::npos);
    EXPECT_TRUE(output.find("8") != std::string::npos);
}

class TeacherTest : public ::testing::Test {
protected:
    Teacher* teacher;
    Subject subject;

    TeacherTest() : teacher(new Teacher(1, "Bob", 40, 15, "doctor")), subject("Math") {}

    ~TeacherTest() {
        delete teacher;
    }
};

TEST_F(TeacherTest, GetID) {
    EXPECT_EQ(teacher->Get_ID(), 1);
}
TEST_F(TeacherTest, AddSubject) {
    teacher->Add_Subject_To_Teacher(subject);

    std::istringstream input("1"); 
    std::cin.rdbuf(input.rdbuf()); 

    EXPECT_NO_THROW({
        Subject & retrieved_subject = teacher->Get_Subject();
        EXPECT_EQ(retrieved_subject.Get_Subject_Name(), subject.Get_Subject_Name()); 
        });

    std::cin.clear(); 
    std::cin.rdbuf(nullptr); 
}

TEST_F(TeacherTest, Info) {
    testing::internal::CaptureStdout();
    teacher->Info();
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("Bob") != std::string::npos);
    EXPECT_TRUE(output.find("doctor") != std::string::npos);
}

class GroupTest : public ::testing::Test {
protected:
    Department* department; 
    Group* group;

    GroupTest() : department(new Department("IIT")), group(new Group(1, department, 1, "AI")) {}

    ~GroupTest() {
        delete group;
        delete department;
    }
};

TEST_F(GroupTest, GetGroupID) {
    EXPECT_EQ(group->Get_Group_ID(), 1);
}

TEST_F(GroupTest, AddStudentToGroup) {
    Student student(1, "Alice", 20);
    group->Add_Student_To_Group(student);
    EXPECT_EQ(group->Get_Group_Size(), 1);
}

TEST_F(GroupTest, Display) {
    testing::internal::CaptureStdout();
    Student student(1, "Alice", 20);
    group->Add_Student_To_Group(student);
    group->Display();
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("Список студентов группы: 1") != std::string::npos);
    EXPECT_TRUE(output.find("Alice") != std::string::npos);
}

TEST_F(GroupTest, DeleteStudentFromGroup) {
    Student student(1, "Alice", 20);
    group->Add_Student_To_Group(student);
    group->Delete_Student_From_Group(0);
    EXPECT_EQ(group->Get_Group_Size(), 0);
}

class AnnouncementTest : public ::testing::Test {
protected:
    Announcement* announcement;

    AnnouncementTest() : announcement(new Announcement("Тестовое объявление", "12345", "11.01.2024")) {}

    ~AnnouncementTest() {
        delete announcement;
    }
};

TEST_F(AnnouncementTest, PrintAnnouncement) {
    testing::internal::CaptureStdout(); 
    announcement->Print();
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("Тестовое объявление") != std::string::npos);
    EXPECT_TRUE(output.find("Автор/ID автора: 12345") != std::string::npos);
    EXPECT_TRUE(output.find("Дата: 11.01.2024") != std::string::npos);
}

class AbsencesTest : public ::testing::Test {
protected:
    Absences* absences;
    Student* student;

    AbsencesTest() : absences(new Absences()), student(new Student(1, "Alice", 20)) {}

    ~AbsencesTest() {
        delete absences;
        delete student;
    }
};

TEST_F(AbsencesTest, InitializeAbsences) {
    absences->Initialize_Absences(*student);
    EXPECT_NO_THROW(absences->Print_Absences(*student));
}

TEST_F(AbsencesTest, AddAbsence) {
    absences->Add_Absence(*student);
    testing::internal::CaptureStdout(); 
    absences->Print_Absences(*student);
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("2") != std::string::npos); 
}

TEST_F(AbsencesTest, DeleteAbsence) {
    absences->Add_Absence(*student); 
    absences->Delete_Absence(*student); 
    testing::internal::CaptureStdout(); 
    absences->Print_Absences(*student);
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("0") != std::string::npos); 
}

TEST_F(AbsencesTest, DeleteAbsenceWhenZero) {
    testing::internal::CaptureStdout(); 
    absences->Delete_Absence(*student); 
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("имеет 0 пропусков") != std::string::npos); 
}

class SalaryTest : public ::testing::Test {
protected:
    Salary* salary;

    SalaryTest() : salary(new Salary()) {}

    ~SalaryTest() {
        delete salary;
    }
};

TEST_F(SalaryTest, DefaultSalaries) {
    EXPECT_EQ(salary->Get_Low_Salary(), 120);
    EXPECT_EQ(salary->Get_Mmedium_Salary(), 170);
    EXPECT_EQ(salary->Get_High_Salary(), 220);
}

TEST_F(SalaryTest, SetLowSalary) {
    int new_low_salary = 150;
    salary->Set_Low_Salary(new_low_salary);
    EXPECT_EQ(salary->Get_Low_Salary(), new_low_salary);
}

TEST_F(SalaryTest, StudentSalaryHigh) {
    testing::internal::CaptureStdout(); 
    salary->Student_Salary(9.0); 
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_TRUE(output.find("Стипендия: 220") != std::string::npos);
}

TEST_F(SalaryTest, StudentSalaryMedium) {
    testing::internal::CaptureStdout();
    salary->Student_Salary(7.0); 
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_TRUE(output.find("Стипендия: 170") != std::string::npos);
}

TEST_F(SalaryTest, StudentSalaryLow) {
    testing::internal::CaptureStdout();
    salary->Student_Salary(5.0); 
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_TRUE(output.find("Стипендия: 120") != std::string::npos);
}

class DepartmentTest : public ::testing::Test {
protected:
    Department* department;

    DepartmentTest() : department(new Department("IIT")) {}

    ~DepartmentTest() {
        delete department;
    }
};

TEST_F(DepartmentTest, GetDepartmentName) {
    EXPECT_EQ(department->Get_Department_Name(), "IIT");
}

TEST_F(DepartmentTest, PrintDepartment) {
    testing::internal::CaptureStdout(); 
    department->Print_Department(); 
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("\nКафедра: IIT") != std::string::npos);
}

class AuthorizationTest : public ::testing::Test {
protected:
    Student* student;
    Teacher* teacher;
    Group* group;
    Department* department;
    Authorization* auth_student;
    Authorization* auth_teacher;

    AuthorizationTest() {
        student = new Student(1, "Alice", 20);
        teacher = new Teacher(1, "Bobh", 40, 15, "doctor");
        department = new Department("Computer Science");
        group = new Group(1, department, 1, "CS");
        auth_student = new Authorization("alice123", "password", student, group);
        auth_teacher = new Authorization("smith123", "password123", teacher);
    }

    ~AuthorizationTest() {
        delete student;
        delete teacher;
        delete group;
        delete department;
        delete auth_student;
        delete auth_teacher;
    }
};

TEST_F(AuthorizationTest, GetStudent) {
    EXPECT_EQ(auth_student->Get_Student(), student);
}

TEST_F(AuthorizationTest, GetGroupForMenu) {
    EXPECT_EQ(auth_student->Get_Group_For_Menu(), group);
}

TEST_F(AuthorizationTest, GetTeacher) {
    EXPECT_EQ(auth_teacher->Get_Teacher(), teacher);
}

TEST_F(AuthorizationTest, GetLogin) {
    EXPECT_EQ(auth_student->Get_Login(), "alice123");
    EXPECT_EQ(auth_teacher->Get_Login(), "smith123");
}

TEST_F(AuthorizationTest, GetPassword) {
    EXPECT_EQ(auth_student->Get_Password(), "password");
    EXPECT_EQ(auth_teacher->Get_Password(), "password123");
}

class TimetableTest : public ::testing::Test {
protected:
    Timetable* timetable;
    Group* group;
    Department* department;
    Subject* math;
    Subject* physics;

    TimetableTest() {
        timetable = new Timetable();
        department = new Department("IIT");
        group = new Group(1, department, 1, "AI");
        math = new Subject("Math");
        physics = new Subject("Physics");
    }

    ~TimetableTest() {
        delete timetable;
        delete group;
        delete department;
        delete math;
        delete physics;
    }
};

TEST_F(TimetableTest, AddSubjectToTimetable) {
    timetable->Add_Subject_To_Timetable(*math, *group);
    timetable->Add_Subject_To_Timetable(*physics, *group);

    testing::internal::CaptureStdout(); 
    timetable->Print_Time_Table(*group);
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("Расписание:") != std::string::npos);
    EXPECT_TRUE(output.find("Math") != std::string::npos);
    EXPECT_TRUE(output.find("Physics") != std::string::npos);
}

TEST_F(TimetableTest, PrintEmptyTimetable) {
    testing::internal::CaptureStdout(); 
    timetable->Print_Time_Table(*group);
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("Занятий в этот день нет") != std::string::npos);
}
class TestableSite : public Site {
public:
    int Get_Authorization_Count() const {
        return authorization.size();
    }

    int Get_Announcements_Count() const {
        return annoucements.size();
    }

    int Get_Groups_Count() const {
        return groups.size();
    }

    int Get_Subjects_Count() const {
        return subjects.size();
    }
};

void RedirectStdInput(const std::string& input) {
    std::istringstream* iss = new std::istringstream(input);
    std::cin.rdbuf(iss->rdbuf());
}

class SiteTest : public ::testing::Test {
protected:
    TestableSite* site;
    Student* student;
    Teacher* teacher;
    Department* department;
    Group* group;
    Subject* subject;
    Announcement* announcement;

    SiteTest() {
        site = new TestableSite();
        student = new Student(1, "Alice", 20);
        department = new Department("IIT");
        teacher = new Teacher(1, "Bob", 40, 15, "doctor");
        group = new Group(1001, department, 1, "AI");
        subject = new Subject("Math");
        announcement = new Announcement("Объявление", "Автор", "01.01.2023");

        group->Add_Subject_To_Group(*subject);
    }

    ~SiteTest() {
        delete site;
        delete student;
        delete teacher;
        delete group;
        delete department;
        delete subject;
        delete announcement;
    }
};

TEST_F(SiteTest, AddStudentAuthorization) {
    std::string login = "alice123";
    std::string password = "password";
    site->Add_Stud_Authorization(login, password, student, group);

    EXPECT_EQ(site->Get_Authorization_Count(), 1);
}

TEST_F(SiteTest, RemoveStudentAuthorization) {
    std::string login = "alice123";
    std::string password = "password";
    site->Add_Stud_Authorization(login, password, student, group);
    EXPECT_EQ(site->Get_Authorization_Count(), 1);

    site->Remove_Student_Authorization(student);
    EXPECT_EQ(site->Get_Authorization_Count(), 0);
}

TEST_F(SiteTest, AddTeacherAuthorization) {
    std::string login = "smith123";
    std::string password = "password123";
    site->Add_Teacher_Authorization(login, password, teacher);

    EXPECT_EQ(site->Get_Authorization_Count(), 1);
}

TEST_F(SiteTest, RemoveTeacherAuthorization) {
    std::string login = "smith123";
    std::string password = "password123";
    site->Add_Teacher_Authorization(login, password, teacher);
    EXPECT_EQ(site->Get_Authorization_Count(), 1);

    site->Remove_Teacher_Authorization(teacher);
    EXPECT_EQ(site->Get_Authorization_Count(), 0);
}

TEST_F(SiteTest, AddGroup) {
    
    std::string input = "1\n"; 
    RedirectStdInput(input);

    site->Add_Group(*group);
    EXPECT_EQ(site->Get_Groups_Count(), 1);
}

TEST_F(SiteTest, DeleteGroup) {

    site->Add_Group(*group);
    EXPECT_EQ(site->Get_Groups_Count(), 1);

    site->Delete_Group();
    EXPECT_EQ(site->Get_Groups_Count(), 0);
}

TEST_F(SiteTest, AddSubject) {

    std::string input = "1\n";
    RedirectStdInput(input);

    site->Add_Subject(*subject);
    EXPECT_EQ(site->Get_Subjects_Count(), 1);
}

TEST_F(SiteTest, DeleteSubject) {

    site->Add_Subject(*subject);
    EXPECT_EQ(site->Get_Subjects_Count(), 1);

    site->Delete_Subject();
    EXPECT_EQ(site->Get_Subjects_Count(), 0);
}

int main(int argc, char** argv) {
    setlocale(LC_ALL, "RU");
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}