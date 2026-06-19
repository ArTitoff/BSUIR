#include "Timetable.h"

void Timetable::Add_Subject_To_Timetable(Subject& subject, Group& group) {
    time_table[group.Get_Group_ID()].push_back(subject);
}

void Timetable::Add_Subject_To_Timetable(const string& subject, Group& group) {
    time_table[group.Get_Group_ID()].emplace_back(subject);
}

void Timetable::Print_Time_Table(Group& group) {
    int i = 0;
    cout << endl << "Расписание:";
    for (const string& day : { "Понедельник", "Вторник", "Среда", "Четверг", "Пятница" }) {
        cout << endl << day << ": ";
        int day = i;
        if (!(day < time_table[group.Get_Group_ID()].size()))
            cout << " Занятий в этот день нет";
        while (day < time_table[group.Get_Group_ID()].size()) {
            cout << time_table[group.Get_Group_ID()][day].Get_Subject_Name() << " ";
            day += 5;
        }
        i++;
    }
}