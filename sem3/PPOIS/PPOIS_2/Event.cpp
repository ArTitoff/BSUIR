#include "Event.h"

Event:: ~Event() {
}
Event::Event(int duration, double rating, string genre, string show_name, int member_amount, int rehearsals_count,
	string premiere_date, string description) :
	duration(duration), rating(rating), genre(genre), show_name(show_name), member_amount(member_amount), rehearsals_count(rehearsals_count),
	premiere_date(premiere_date), description(description) {}