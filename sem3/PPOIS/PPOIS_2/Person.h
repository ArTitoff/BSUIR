#pragma once
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include "Exceptions.h"

using namespace std;

class Person {
protected:
	string name;
	int age;
public:
	Person(string name, int age);
	virtual void Info();
	virtual ~Person();
	string Get_Name();
};