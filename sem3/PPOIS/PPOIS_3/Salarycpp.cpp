#include "Salary.h"

void Salary::Student_Salary(const double& av_grade) {
    if (av_grade > 8)
        cout << "Стипендия: " << high_salary << endl;
    else if (av_grade < 8 && av_grade > 6)
        cout << "Стипендия: " << medium_salary << endl;
    else  cout << "Стипендия: " << low_salary << endl;
}

void Salary::Set_Low_Salary(int& low_salary) {
    this->low_salary = low_salary;
}
void Salary::Set_Medium_Salary(int& medium_salary) {
    this->medium_salary = medium_salary;
}
void Salary::Set_High_Salary(int& high_salary) {
    this->high_salary = high_salary;
}
int Salary::Get_Low_Salary() {
    return low_salary;
}
int Salary::Get_Mmedium_Salary() {
    return medium_salary;
}
int Salary::Get_High_Salary() {
    return high_salary;
}