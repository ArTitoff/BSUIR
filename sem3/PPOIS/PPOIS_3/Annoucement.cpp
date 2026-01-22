#include "Annoucement.h"

Announcement::Announcement(const string& text, const string& author_id, const string& date) :
    text(text), author_id(author_id), date(date) {}
void Announcement::Print() {
    cout << endl << text << endl << "\nАвтор/ID автора: " << author_id << "\nДата: " << date << endl;
}