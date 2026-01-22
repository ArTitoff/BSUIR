#include "Subject.h"

Subject::Subject(string subject_name) :
    subject_name(subject_name) {}

string Subject::Get_Subject_Name() {
    return subject_name;
}