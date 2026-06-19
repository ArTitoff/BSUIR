#include <iostream>
using namespace std;

struct obj {
	int data;
	obj* prev, * next;
};

void FirstElem(obj** begin, obj** end, int data) {
	obj* ptr = new obj;
	ptr->data = data;
	ptr->next = ptr->prev = NULL;
	*begin = *end = ptr;
}

void pushBegin(obj** begin, int data) {
	obj* ptr = new obj;
	ptr->data = data;
	ptr->prev = NULL; // Предыдущего нет
	ptr->next = *begin; // Связываем новый элемент с первым
	(*begin)->prev = ptr; // Изменяем адрес prev бывшего первого
	(*begin) = ptr;

}

void pushEnd(obj** end, int data) {
	obj* ptr = new obj;
	ptr->data = data;
	ptr->next = NULL; // Следующего нет
	ptr->prev = *end; // Связываем новый с последним
	(*end)->next = ptr; // Изменяем адрес next бывшего последнего
	*end = ptr;
}

void viewFromBegin(obj* t) {
	while (t != NULL) {
		cout << t->data << endl;
		t = t->next;
	}
}

void viewFromEnd(obj* t) {
	while (t != NULL) {
		cout << t->data << endl;
		t = t->prev;
	}
}


void DelEvery2(obj* top, obj** end) {
	obj* temp = top;
	int k = 1;
	while (top != NULL) {
		obj* nextNode = top->next;
		if (k % 2 == 0) {
			delete top;
			temp->next = nextNode;
			if (nextNode != NULL)
			nextNode->prev = temp;
			top = nextNode;
		}
		else {
			temp = top;
			top = nextNode;
		}
		k++;
	}
	*end = temp;
}

void out(obj** begin, obj** end, int out) {
	obj* t = *begin;
	while (t != NULL) {
		if (out == t->data) {
			if (t->prev == NULL) {
				*begin = t->next;
				delete t;
				(*begin)->prev = NULL;
			}
			else if (t->next == NULL) {
				*end = t->prev;
				delete t;
				(*end)->next = NULL;
			}
			else {
				(t->prev)->next = t->next;
				(t->next)->prev = t->prev;
				delete t;
			}
			break;
		}
		t = t->next;
	}
	if (t == NULL) cout << "Такого элемента нет" << endl;
}

void del(obj** top) {
	obj* t;

	while (*top != NULL) {
		t = *top;
		*top = (*top)->next;
		delete t;
	}
}

int main() {
	obj* begin = NULL;
	obj* end = NULL;
	FirstElem(&begin, &end, 1);
	pushEnd(&end, 2);
	pushEnd(&end, 3);
	pushEnd(&end, 4);
	viewFromBegin(begin);
	int b = 52;
	int* a = &b;
	//top = out(top, a);
	//cout << b;
	DelEvery2(begin, &end);
	cout << "\n------------------------" << endl;
	//out(&begin, &end, 3);
	viewFromBegin(begin);

	del(&begin);
	viewFromBegin(begin);
	return 0;

}
	/*
int main() {
	int a = 243;
	int l = a % 100;
	cout << l;
	return 0;
}
*/