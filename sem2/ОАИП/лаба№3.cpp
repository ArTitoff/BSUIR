#include <iostream> 
#include <iomanip> 
#include <cmath>
using namespace std;
int main()
{
	 double a, b, h, x, y, s, p;
	int n, i;
	cout << "Vvedite a,b,n" << endl;
	
	while (!(cin >> a) || !(cin >> b) || !(cin >> n)) {
		cin.clear();
		cin.ignore(cin.rdbuf()->in_avail());
		cout << "Vvedite vse chisla zanovo ";
	}

	h = (b-a)/ 10;
	x = a;
	do
	{
		p = s = x/6;
		for (i = 2; i <= n; i++)
		{
			p = p * pow(i,2) * x/(2*i+1)/(2*i)/pow(i-1,2);
			s += p;
		}
		y = ((x+1)/pow(x,1/2.)*sinh(pow(x,1/2.))-cosh(pow(x, 1 / 2.))) / 4;
		cout << setw(15) << x << setw(15) << y << setw(15) << s << endl;
		x += h;
	} while (x <= b + h / 2);
	cout << endl;
	return 0;
}

#include <iostream> 
int main() {
	int N;
	cin >>N;
	int arr[N];
	for (int i = 0; i < N; i++)
		cin >> arr[i];
	int t, j, k = 0;
	for (int i = 0; i < N; i++) {
		if ((i mod 2 == 0 and arr[i] mod 2 != 0) or (i mod 2 != 0 and arr[i] mod 2 == 0)){
			if (k < 1)
				j = i;
			else t = i;
			k++;
	
		}
		if (k > 2) {
			cout << "-1 -1";
			return 0;
		}
	}
	if (k == 1 or k == 0 or (arr[t] + arr[j]) mod 2 == 0) {
		cout << "-1 -1";
		return 0;
	}
	else {
		cout << arr[t] << ' ' << arr[j];
	}
	return 0;
	
}
