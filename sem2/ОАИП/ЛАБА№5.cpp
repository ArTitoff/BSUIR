/*#include <iostream>
using namespace std;

void swapRows(int **arr, int row1, int row2, int cols) {
    for (int i = 0; i < cols; i++) {
        int temp = arr[row1][i];
        arr[row1][i] = arr[row2][i];
        arr[row2][i] = temp;
    }
}

void printArray(int ** arr, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            cout << arr[i][j] << " ";
        }
        cout << endl;
    }
}

int main() {
    int ROWS, COLS, imax=0,imin=0,jmin=0,jmax=0;
    cout << "Введите количество строк и столбцов: ";
    cin >> ROWS >> COLS;
    int** arr = new int* [ROWS];
    for (int i = 0; i < ROWS; i++) {
        arr[i] = new int[COLS];
    }

    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            cin >> arr[i][j];
            if (arr[i][j] > arr[imax][jmax])  imax = i;  
            if (arr[i][j] < arr[imin][jmin])  imin = i;  
        }
    }
    
    
    cout << "Исходный массив:\n";
    printArray(arr, ROWS, COLS);

    swapRows(arr, imax, imin, COLS);

    cout << "Массив после замены строк:\n";
    printArray(arr, ROWS, COLS);


    for (int i = 0; i < ROWS; i++) {
        delete [] arr[i];
    }
    delete[] arr;
    return 0;
}


#include <iostream>
using namespace std;
int main() {
    int n, m;
    cin >> n >> m;
    int** arr = new int* [n];
    for (int i = 0; i < m; i++) {
        arr[i] = new int[m];
    }
    int sum=0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> arr[i][j];
            if (i == 0 || i == n-1 || j == 0 || j == m-1)
                arr[i][j] = arr[i][j] * arr[i][j];
            if (i == 1 && arr[i][j]<0)
            sum += arr[i][j];
        }
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cout << arr[i][j] << '\t';
        }
       cout << endl;
    }
    cout << endl << sum;
    for (int i = 0; i < m; i++) {
        delete[] arr[i];
    }
    delete[] arr;
    return 0;
}



#include <iostream>
#include <iomanip> 
#include <math.h> 
using namespace std;
void fuc(double x, double* y)
{
    *y = (2.0 * (x) * (x)-1) * exp(x);


}
int main()
{
    double x, y;


    for (x = 0.2; x <= 0.9; x += 0.073)
    {
        fuc(x, &y);
        cout << setw(15) << x << setw(15) << y << endl;
    }

    cout << endl;
    return 0;
}


#include <iomanip>
#include <iostream>
using namespace std;
//??????????????
int main() {
    int N;
    int sum = 0;
    int k = 1;
    cin >> N;
    int* A = new int[N];
    int* b = new int[k];
    for (int i = 0; i < N; i++) {
        cin >> A[i];
    }
    cout << endl;
    for (int i = 0; i < N; i++) {
 
        if (A[i] > 0)
            sum += A[i];
        if (A[i] < 0)
            A[i] *= 4;
            cout << A[i] << ' ';
    }
    cout << endl << "SUMMA - " << sum << endl;

    for (int i = 1; i < N-1; i++) {
        if (A[i - 1] + A[i + 1] > 12) {
            b[k-1] = i;
            k++;
        }
    }
    cout << endl << "Last massiv : ";

    for (int i = 0; i < N; i++) {
        bool cho = true;
        for (int j = 0; j < k - 1 ; j++) {
            if (i == b[j]) {
                cho = false;
            }
        }
        if (cho) {
            cout << A[i] << ' ';
        }
    }
    delete[] b;
    delete[] A;
    return 0;
} 

#include <iostream>
using namespace std;
int main() {
    int n;
    double sum = 0;
    cin >> n;
    double* arr = new double[n];
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
        if (i % 2 != 0) {
            sum += arr[i];
        }
    }
    for (int i = 0; i < n; i++) {
        if (arr[i] < 0)
            arr[i] = 0;
        cout << arr[i] << ' ';
    }
    cout << endl << "Summa = " << sum << endl;
    for (int i = 1; i < n - 1; i++) {
        if (arr[i] == 0)
            arr[i] = (arr[i + 1] + arr[i - 1]) / 2;
    }
    cout << " NEW MASS " << endl;
    for (int i = 0; i < n; i++) {
        cout << arr[i] << ' ';
    }
    delete[] arr;
    return 0;
} */