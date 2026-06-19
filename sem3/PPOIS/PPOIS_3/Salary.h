#pragma once
#include <iostream>
using namespace std;

class Salary {
protected:
    int low_salary = 120;
    int medium_salary = 170;
    int high_salary = 220;
public:
    void Student_Salary(const double& av_grade);

    void Set_Low_Salary(int& low_salary);
    void Set_Medium_Salary(int& medium_salary);
    void Set_High_Salary(int& high_salary);
    int Get_Low_Salary();
    int Get_Mmedium_Salary();
    int Get_High_Salary();
};