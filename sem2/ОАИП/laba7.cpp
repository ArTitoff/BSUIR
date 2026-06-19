#define _USE_MATH_DEFINES
#include <iostream> 
#include <math.h> 
#include <iomanip>

using namespace std;

typedef double (*uf)(double, double, int&);
void Tabl(double, double, double, double);
double Y(double);
double S(double, double, double, int&);

int main()
{
	//Tabl(-0.8, 0.9, 0.1, 0.0001);
	Tabl(1, 2.5, 0.1, 0.0001);
	cout << endl;
	/*cout << setw(12) << "x" << setw(15) << "s(x)" << setw(5) << "k" << endl;
	tabl(-0.8, 0.9, 0.1, 0.0001, s);*/
	return 0;
}

void Tabl(double a, double b, double h, double eps) {

	cout << setw(12) << "x" << setw(15) << "y(x)" << setw(15) << "s(x)" << setw(5) << "k" << endl;

	for (double x = a; x < b + h / 2; x += h)
	{
		int k = 0;
		double y = Y(x);
		double s = S(x, y, eps, k);
		cout << setw(12) << x << setw(15) << y << setw(15) << s << setw(5) << k << endl;
	}
}

double Y(double x)
{
	//return pow(x + 1, 1 / 4.) - (4 - x) / 4.0;
	return (3 * pow(x, 2) - 6 * M_PI * x + 2 * M_PI * M_PI) / 12.0;
}

double S(double x, double y, double eps, int& k)
{
	//double p = 1 * x / (4.0 * 2);
	//double sum = 0;
	////p = sum = pow(-1, 1) * (4 * 2 - 5) * (4 * 2 - 7) / (4 * 2 - 2) / (4 * 2) * pow(x, 2);
	//for (int i = 2; i <= 100; i++)
	//{
	//	p *= ((4.0 * i - 5) * (4 * i - 7)) / ((4 * i) * (4 * i - 2));
	//	p *= (-1) * x;
	//	sum += p;
	//	if (fabs(sum - y) < eps)
	//	{
	//		k = i;
	//		return sum;
	//	}
	//}
	//return -1;

	//double p = 1;
	double sum = 0;
	for (int i = 1; i <= 100; i++)
	{
		//p *= ((4.0 * i - 5) * (4 * i - 7)) / ((4 * i) * (4 * i - 2));
		sum += cos(i * x) / (i * i);
		if (fabs(sum - y) < eps)
		{
			k = i;
			return sum;
		}
	}
	return -1;
}
