#pragma once
#include "Group.h"

class Timetable {
protected:
    map<int, vector<Subject>> time_table;
public:
    void Add_Subject_To_Timetable(Subject& subject, Group& group);

    void Add_Subject_To_Timetable(const string& subject, Group& group);

    void Print_Time_Table(Group& group);

};