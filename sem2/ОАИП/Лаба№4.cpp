/* #include <iostream>

using namespace std;

int main()
{
	setlocale(LC_ALL, "RU");
	int n,j;
	cin >> n;

	int* a = new int[n];
	for (int i = 0; i < n; i++) 
		cin >> a[i];

	for (int i = 0; i < n; i++)
        if (a[i] < 0)
        {
            for (j = i + 1; j < n; j++) 
                a[j - 1] = a[j];
            
            n--; i--;
		}

	for (j = 0; j < n; j++) 
		cout << a[j] << endl;
	

	delete[] a;
	return 0;
} 

#include <iostream>
using namespace std;

int main() {
    setlocale(LC_ALL, "RU");
 

    int k;
    do {
        cout << "Vvedite razmer massiva ";
        while (!(cin >> k)) {
            cin.clear();
            cin.ignore(cin.rdbuf()->in_avail());
            cout << "Vvedite chislo ";
        }
        
    } while (k > 100);

    int* mas = new int[k];
    cout << "Vvedite elementi massiva ";
    for (int i = 0; i < k; i++)
    {
        while (!(cin >> mas[i])) {
            cin.clear();
            cin.ignore(cin.rdbuf()->in_avail());
            cout << "Vvedite chislo ";
        }
    }
    cout << "ishodni massiv ";
    for (int i = 0; i < k; i++)
    {
        cout << mas[i] << " ";
    }
    int count = 0;
    for (int i = 0; i < k; i++)
    {
        int j = 0;
        while (j < i && mas[j] != mas[i]) j++;

        count += j == i;
    }
    cout << endl;
    cout << "Unikalnih elementov " << count << endl;
    delete[] mas;
   

    return 0;
}


#include <iostream>

using namespace std;

int main() {
    int n;
    cin >> n;
    int* arr = new int[n];
    for (int i = 0; i < n; i++)
        cin >> arr[i];
    int k=1;
    for (int i = 0; i < n; i++) {
        if (k % 3 == 0) {
            for (int j = i ; j < n; j++) {
                arr[j] = arr[j + 1];
            }
            i--;
            n--;
        }
        k++;
    }

    for (int i = 0; i < n; i++)
        cout << arr[i];
    return 0;
}*/
#include <iostream>
#include <algorithm> 

using namespace std;

int main() {
    setlocale(LC_ALL, "RU");
    const int SIZE = 8;
    int A[SIZE], B[SIZE], C[SIZE];
    int countEqualToB2 = 0;

    cout << "Введите элементы массива A (8 элементов):" << endl;
    for (int i = 0; i < SIZE; i++) {
        cin >> A[i];
    }

    cout << "Введите элементы массива B (8 элементов):" << endl;
    for (int i = 0; i < SIZE; i++) {
        cin >> B[i];
    }

    for (int i = 0; i < SIZE; i++) {
        C[i] = min(4 * A[i], B[i] * B[i]);
        if (C[i] == B[i] * B[i]) {
            countEqualToB2++;
        }
    }

    cout << endl << "Массив A: ";
    for (int i = 0; i < SIZE; i++) {
        cout << A[i] << " ";
    }

    cout << endl  << "Массив B: ";
    for (int i = 0; i < SIZE; i++) {
        cout << B[i] << " ";
    }

    cout << endl << "Массив C: ";
    for (int i = 0; i < SIZE; i++) {
        cout << C[i] << " ";
    }

    cout << endl << "Количество элементов C, равных B[i]^2: " << countEqualToB2 << endl;

    return 0;
}