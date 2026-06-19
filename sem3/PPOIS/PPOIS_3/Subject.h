#pragma once
#include "Data_Exception.h"

class Subject {
protected:
    string subject_name;

public:
    Subject(string subject_name);

    string Get_Subject_Name();
};