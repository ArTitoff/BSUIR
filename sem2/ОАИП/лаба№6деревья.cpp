// лаба№6деревья.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include <string>

using namespace std;

struct Tree
{
	int info;

	string name;

	Tree* left;

	Tree* right;

	Tree(string str, int val) : name(str), info(val), left(nullptr), right(nullptr) {}


};

void Add(Tree*& current, string str, int value) {
	if (!current) {
		current = new Tree(str, value);
		return;
	}
	else
		if (value < current->info) {
			Add(current->left, str, value);
		}
		else if (value > current->info)
		{
			Add(current->right, str, value);
		}
		else 	return;
}

void print(Tree* node) {
	if (!node) return;
	else
	print(node->left);
	cout << node->name << " " << node->info << "   ";
	print(node->right);
}

void deb(Tree* node) {
	if (!node) return;

	deb(node->left);
	//cout << node->name << " " << node->info << " ";
	deb(node->right);
	delete node;
}

void printTree(Tree* root, int level) {
    if (root == nullptr) {
        return;
    }

    printTree(root->right, level + 1);

    for (int i = 0; i < level; ++i) {
        std::cout << "   ";
    }
    std::cout << root->name << " " << root->info << std::endl;

    printTree(root->left, level + 1);
}

Tree* Del_Info(Tree* root, int key) {
	Tree* Del, * Prev_Del, * R, * Prev_R;
	// Del, Prev_Del – удаляемый узел и его предыдущий (предок);
	// R, Prev_R – элемент, на который заменяется удаленный узел, и его предок;
	Del = root;
	Prev_Del = NULL;
	//-------- Поиск удаляемого элемента и его предка по ключу key ---------
	while (Del != NULL && Del->info != key) {
		Prev_Del = Del;
		if (Del->info > key) Del = Del->left;
		else Del = Del->right;
	}
	if (Del == NULL) { // Элемент не найден
		cout << "Not key!";
		return root;
	}
	//-------------------- Поиск элемента R для замены --------------------------------
	if (Del->right == NULL) R = Del->left;
	else
		if (Del->left == NULL) R = Del->right;
		else {
			//---------------- Ищем самый правый узел в левом поддереве -----------------
			Prev_R = Del;
			R = Del->left;
			while (R->right != NULL) {
				Prev_R = R;
				R = R->right;
			}
			//----------- Нашли элемент для замены R и его предка Prev_R -------------
			if (Prev_R == Del) R->right = Del->right;
			else {
				R->right = Del->right;
				Prev_R->right = R->left;
				R->left = Prev_R;
			}
		}
	if (Del == root) root = R; // Удаляя корень, заменяем его на R
	else
		//------- Поддерево R присоединяем к предку удаляемого узла -----------
		if (Del->info < Prev_Del->info)
			Prev_Del->left = R; // На левую ветвь
		else Prev_Del->right = R; // На правую ветвь
	delete Del;
	return root;
}

void massadd(Tree* root, int a[], string b[], int& k) {
	if (root == NULL)
		return;
	massadd(root->left, a, b, k);
	a[k - 1] = root->info;
	b[k - 1] = root->name;
	k++;
	massadd(root->right, a, b, k);
}

void Make_Blns(Tree** p, int n, int k, int* a, string * b) {
	if (n == k) {
		*p = NULL;
		return;
	}
	else {
		int m = (n + k) / 2;
		 *p = new Tree(b[m], a[m]);
		(*p)->info = a[m];
		Make_Blns(&(*p)->left, n, m, a, b);
		Make_Blns(&(*p)->right, m + 1, k, a, b);
	}
}


void UP_DOWN(Tree* root) {
	if (root != nullptr) {
		cout << root->name << " " << root->info << "   ";
		UP_DOWN(root->left);
		UP_DOWN(root->right);
	}
}

void LEFT_RIGHT(Tree* root) {
	if (root != nullptr) {
		LEFT_RIGHT(root->left);
		cout << root->name << " " << root->info << "   ";
		LEFT_RIGHT(root->right);
	}
}

void DOWN_UP(Tree* root) {
	if (root != nullptr) {
		DOWN_UP(root->left);
		DOWN_UP(root->right);
		cout << root->name << " " << root->info << "   ";
	}
}

void RESH(Tree* root, int& k) {
	if (root == nullptr)
		return;
	RESH(root->left, k);
	RESH(root->right, k);
	k++;
}

int main()
{	
	Tree* root = NULL; 
        string data[][2] = { {"Smi", "7"}, {"Joh", "4"}, {"Wil", "9"}, {"Gig", "2"}, {"Smt", "5"} };

    for (auto& d : data) {
        Add(root, d[0], stoi(d[1]));
    }

	printTree(root, 0);

	Add(root, "New", 10);
	Add(root, "Yur", 8);

	cout << endl << "После добавления" << endl << endl;

	printTree(root, 0);

	cout << endl << "---------------------" << endl;
	cout << endl << endl << "Слева-направо "  << endl;
	print(root);
	cout << endl << endl  << "Сверху-вниз "  << endl;
	UP_DOWN(root);
	cout << endl << endl << "Снизу-вверх " << endl;
	DOWN_UP(root);
	int l = 0;
	RESH(root->left, l);
	cout << endl << endl << endl << "Количество записей в левом поддереве: " << l << endl;


	cout << endl << endl << "После удаления " << endl << endl;
	Del_Info(root, 9);
	Del_Info(root, 8);
	printTree(root, 0);

	int kolel = 1;
	int* a = new int[kolel];
	string b[6];

	massadd(root, a, b , kolel);

	Make_Blns(&root, 0, 5, a, b);

	cout << endl << endl << "После балансировки " << endl << endl;

	printTree(root, 0);

	//deb(root);
	//print(root);
}
