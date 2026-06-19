#pragma once
#include <iostream>
#include <string>
using namespace std;

class Announcement {
protected:
    string text;
    string author_id;
    string date;
public:
    Announcement(const string& text, const string& author_id, const string& date);
    void Print();
};