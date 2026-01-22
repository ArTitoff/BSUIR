#include <iostream>
using namespace std;
struct obj {
	int data;
	obj* next;
};
obj* push(obj* top, int data) {
	obj* ptr = new obj;
	ptr->data = data;
	ptr->next = top;
	return ptr;
}
void view(obj* t) {	
	while (t != NULL) {
		cout << t->data << endl;
		t = t->next;
	}
}

/* void view1(obj* top) {
	obj* t ;
	int k = 1;
	while (top != NULL) {
		t = top;
		top = top->next;
		if (k % 2 == 0)
			delete t;
		k++;
		
		
	}
}*/
void DelEvery2(obj* top) {
	obj* temp = top;
	int k = 1;
	while (top!= NULL) {
		obj* nextNode = top->next;
		if (k % 2 == 0) {
			delete top;
			temp->next = nextNode;
			top = nextNode;
		}
		else {
			temp = top;
			top = nextNode;
		}
		k++;
	}
}

obj* out(obj* top, int* out) {
	obj* t = top;
	*out = top->data;
	top = top->next;
	delete t;
	return top;
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
	obj* top = NULL;
	top = push(top, 1);
	top = push(top, 2);
	top = push(top, 3);
	top = push(top, 4);
	top = push(top, 5);
	top = push(top, 6);
	view(top);
	int b = 52;
	int* a = &b; 
	//top = out(top, a);
	//cout << b;
	DelEvery2(top);
	cout << "\n------------------------" << endl;
	view(top);
	
	del(&top);
	view(top);
	return 0;
}