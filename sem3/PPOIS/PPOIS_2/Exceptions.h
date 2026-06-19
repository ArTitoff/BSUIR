#pragma once
#include <iostream>

using namespace std;

class Data_Exception : public runtime_error {
public:
	Data_Exception(const string& msg) : runtime_error(msg) {}
};

class Value_Exception : public runtime_error {
public:
	Value_Exception(const string& msg) : runtime_error(msg) {}
};