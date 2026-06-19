#include <iostream>
#include <cmath>

using namespace std;
int main() {
	int n,e;
	int k = 0;
	cin >> n;
	e = n;
	char* a = new char [n];
	char* b = new char[e];
	for (int i = 0; i < n; i++) {
		cin >> a[i];
	}

		for (int i = 0; i < n; i++) {
			if (isdigit(a[i])) {
				b[k] = a[i];
				k++;
				for (int j = i + 1; j < n; j++) {
					a[j - 1] = a[j];
				}
				i--;
				n--;
			}	
		
		}
		
		for (int i = 0; i < n; i++) {
			b[k + i] = a[i];
		}

		for (int i = 0; i < e; i++) {
			cout << b[i] << endl;
		}

		delete [] a;
		delete[] b;
	return 0;
}