#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <iomanip>
#include "Site.h"

using namespace std;

/*
int main()
{
    setlocale(LC_ALL, "RU");

    Subject mo("Math");
    Subject bio("Bio");
    Student bob(3219, "Bob", 24);
    Student lob(3218, "Lesha", 24);
    Student stud(3217, "Artem", 18);
    Student stud2(3226, "Albert", 20);
    bob.Add_Grade(mo, 4);
    bob.Add_Grade(mo, 6);
    bob.Add_Grade(bio, 7);
    lob.Add_Grade(mo, 5);
    Department dep("IIT");
    Department dep1("ITAS");
    Group a(3223, &dep, 2, "AI");  
    a.Add_Student_To_Group(stud2);
    a.Add_Student_To_Group(bob);
    a.Add_Student_To_Group(lob);
    a.Add_Student_To_Group(stud);
    Teacher t(1234, "Prooo", 30, 5, "aspirant");
    t.Add_Subject_To_Teacher(mo);

    Timetable tim;

    tim.Add_Subject_To_Timetable("Hist", a);
    tim.Add_Subject_To_Timetable("Engl", a);
    tim.Add_Subject_To_Timetable("Rus", a);
    tim.Add_Subject_To_Timetable("Chem", a);
    tim.Add_Subject_To_Timetable(bio, a);
    tim.Add_Subject_To_Timetable(mo, a);
    //Absences ab;
    //ab.Add_Absence(bob);
    //ab.Add_Absence(lob);
    //ab.Add_Absence(lob);
    Site site;
    site.Add_Department(dep);
    site.Add_Department(dep1);
    site.Add_Group(a);
    site.Add_Teacher(t);
    site.Add_Subject(mo);
    site.Add_Subject(bio);
    a.Add_Subject_To_Group(mo);
    a.Add_Subject_To_Group(bio);
    site.Timetable_Of_Group(a);
    string login = "22";
    string pas1 = "22";
    string pas2 = "23";
    string pas3 = "24";
    string pas4 = "25";
    string pas5 = "26";
    site.Add_Stud_Authorization(login, pas1, &bob, &a);
    site.Add_Stud_Authorization(login, pas2, &lob, &a);
    site.Add_Stud_Authorization(login, pas3, &stud, &a);
    site.Add_Stud_Authorization(login, pas4, &stud2, &a);
    site.Add_Teacher_Authorization(login, pas5, &t);
    site.Main_Menu();
}

*/
