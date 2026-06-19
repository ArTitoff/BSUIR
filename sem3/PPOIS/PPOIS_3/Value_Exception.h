#pragma once
#include "Data_Exception.h"

class Value_Exception : public runtime_error {
public:
    Value_Exception(const string& msg) : runtime_error(msg) {}
};

void  Correct_Cin(int& param, int value1, int value2);