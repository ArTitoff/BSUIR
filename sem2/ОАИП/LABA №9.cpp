#include <iostream>
using namespace std;
int faktorial(int k, int n) {
	if (k == n) return 1;
	if (k == 1) return n;
	
	return faktorial(k - 1, n - 1) + faktorial(k, n - 1);
}

int main()
{
	int k, n;
	cin >> k >> n;
	cout << endl;
	cout << faktorial(k, n);
	return 0;
}

