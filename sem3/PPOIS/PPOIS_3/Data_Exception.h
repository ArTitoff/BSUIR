#pragma once
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <iomanip>

using namespace std;

class Data_Exception : public runtime_error {
public:
    Data_Exception(const string& msg) : runtime_error(msg) {}
};

void  Correct_Date(string& pub_date);