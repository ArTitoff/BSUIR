#include <iostream>
#include <string>
#include <cmath>

using namespace std;

struct Stack {
    char info; // Информационная часть элемента, например, int
    Stack* next; // Адресная часть – указатель на следующий элемент
};  // Указатель вершины стека

Stack* InStack(Stack* p, char in) {
    Stack* t = new Stack; // Захватываем память для элемента
    t->info = in; // Формируем информационную часть
    t->next = p; // Формируем адресную часть
    return t;
}

Stack* OutStack(Stack* p, char* out) {
    Stack* t = p; // Устанавливаем указатель t на вершину p
    *out = p->info;
    p = p->next; // Переставляем вершину p на следующий элемент
    delete t; // Удаляем бывшую вершину t
    return p; // Возвращаем новую вершину p
}

/*struct Stack1 {
    string info; // Информационная часть элемента, например, int
    Stack1* next; // Адресная часть – указатель на следующий элемент
};  // Указатель вершины стека

Stack1* InStack1(Stack1* p, string in) {
    Stack1* t = new Stack1; // Захватываем память для элемента
    t->info = in; // Формируем информационную часть
    t->next = p; // Формируем адресную часть
    return t;
}

Stack1* OutStack1(Stack1* p, string* out) {
    Stack1* t = p; // Устанавливаем указатель t на вершину p
    *out = p->info;
    p = p->next; // Переставляем вершину p на следующий элемент
    delete t; // Удаляем бывшую вершину t
    return p; // Возвращаем новую вершину p
}*/
struct Stack1 {
    string data;
    Stack1* next;
};

Stack1* InStack1(Stack1* top, string ch) {
    Stack1* newNode = new Stack1();
    newNode->data = ch;
    newNode->next = top;
    return newNode;
}

Stack1* OutStack1(Stack1* top, string* ch) {
    Stack1* temp = top;
    *ch = temp->data;
    top = top->next;
    delete temp;
    return top;
}

int Prior(char a) {
    switch (a) {
    case '^': return 4;
    case '*': case '/': return 3;
    case '-': case '+': return 2;
    case ')': return 1;
    }
    return 0;
}


int main()
{
    string primer = "(a + b * c) / (d - e) ";
    string OutStr = "";
    size_t len = primer.size();
    Stack* begin = NULL;
    char ss, a;
    for (int i = 0; i < len; i++) {
        ss = primer[i];
        // Открывающую скобку записываем в стек
        if (ss == '(') begin = InStack(begin, ss);
        if (ss == ')') {
            // Выталкиваем из стека все знаки операций до открывающей скобки
            while ((begin->info) != '(') {
                begin = OutStack(begin, &a); // Считываем элемент из стека
                OutStr += a; // Записываем в строку
            }
            begin = OutStack(begin, &a); // Удаляем из стека '(' скобку
        }
        // Букву (операнд) заносим в выходную строку
        if (ss >= 'a' && ss <= 'z') OutStr += ss;
        /* Если знак операции, то переписываем из стека в выходную строку все
        операции с большим или равным приоритетом */
        if (ss == '+' || ss == '-' || ss == '*' || ss == '/' || ss == '^') {
            while (begin != NULL && Prior(begin->info) >= Prior(ss)) {
                begin = OutStack(begin, &a);
                OutStr += a;
            }
            begin = InStack(begin, ss);
        }
    }
    // Если стек не пуст, переписываем все операции в выходную строку
    while (begin != NULL) {
        begin = OutStack(begin, &a);
        OutStr += a;
    }
    cout << OutStr << "   - польская запись" << endl;   // Выводим полученную строку

    
   
    /*string ch = "", ch1 = "", ch2 = "";
    double op1=0, op2=0, rez=0;
    string chr ="";
    Stack1* begin1 = NULL;
    for (int i = 0; i < OutStr.size(); i++) {
        ch = OutStr[i];
        if (ch != "*" && ch != "-" && ch != "+" && ch != "/" && ch != "^") begin1 = InStack1(begin1, ch);
        else {
            begin1 = OutStack1(begin1, &ch1);
            begin1 = OutStack1(begin1, &ch2);
            if (ch1 == "a" || ch1 == "b" || ch1 == "c" || ch1 == "d" || ch1 == "e") {
                cout << "Введите число " << ch1 << " ";
                cin >> op1;
            }
            else 
                op1 = stod(ch1);
            
            if (ch2 == "a" || ch2 == "b" || ch2 == "c" || ch2 == "d" || ch2 == "e") {
                cout << "Введите число " << ch2 << " ";
                cin >> op2;
            }
            else
                op2 = stod(ch2);
            
            if (ch == "+") {
                rez = op2 + op1; 
            }
            if (ch == "-") {
                rez = op2 - op1;
            }
            if (ch == "*") {
                rez = op2 * op1; 
            }
            if (ch == "/") {
                rez = op2 / op1; 
            }
            if (ch == "+") {
                rez = pow(op2, op1); 
            }
            chr = to_string(rez);
            begin1 = InStack1(begin1, chr);
        }
    }
        cout << rez << " pri";*/
    Stack1* begin1 = NULL;

    for (int i = 0; i < OutStr.size(); i++) {
        string ch = string(1, OutStr[i]);
        if (ch != "*" && ch != "-" && ch != "+" && ch != "/" && ch != "^") {
            begin1 = InStack1(begin1, ch);
        }
        else {
            string ch1, ch2;
            begin1 = OutStack1(begin1, &ch1);
            begin1 = OutStack1(begin1, &ch2);

            double op1, op2, rez;

            if (ch1 == "a" || ch1 == "b" || ch1 == "c" || ch1 == "d" || ch1 == "e") {
                cout << "Введите число " << ch1 << " ";
                cin >> op1;
            }
            else {
                op1 = stod(ch1);
            }

            if (ch2 == "a" || ch2 == "b" || ch2 == "c" || ch2 == "d" || ch2 == "e") {
                cout << "Введите число " << ch2 << " ";
                cin >> op2;
            }
            else {
                op2 = stod(ch2);
            }

            if (ch == "+") {
                rez = op2 + op1;
            }
            else if (ch == "-") {
                rez = op2 - op1;
            }
            else if (ch == "*") {
                rez = op2 * op1;
            }
            else if (ch == "/") {
                rez = op2 / op1;
            }
            else if (ch == "^") {
                rez = pow(op2, op1);
            }

            string chr = to_string(rez);
            begin1 = InStack1(begin1, chr);
        }
    }

    string resultStr;
    begin1 = OutStack1(begin1, &resultStr);
    double result = stod(resultStr);
    cout << "Результат: " << result << endl;

    return 0;
}
