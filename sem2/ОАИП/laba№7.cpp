#include <iostream> 
#include <string> 
using namespace std;

int main()
{
	struct strc {
		string fio;
		int otc[4];
		double sb;
	};

	strc mstud[100];
	int nst, i, j;
	cout << "Vvedite kol-vo studentov" << endl;
	cin >> nst;

	for (i = 0; i < nst; i++)
	{
		cout << "Vvedite FIO" << endl;
		getline(cin >> ws, mstud[i].fio);
		cout << "Vvedite 4 otcenki" << endl;
		mstud[i].sb = 0;
		for (j = 0; j < 4; j++)
		{
			cin >> mstud[i].otc[j];
			mstud[i].sb += mstud[i].otc[j] / 4.;
		}
		cout << endl;
	}
	double srb=0;
	for (i = 0; i < nst; i++) {
		srb +=mstud[i].sb;
	}
	srb = srb / nst;
	strc stemp;
	for (i = 0; i < nst - 1; i++)
		for (j = i + 1; j < nst; j++)
			if (mstud[i].sb < mstud[j].sb)
			{
				stemp = mstud[i];
				mstud[i] = mstud[j];
				mstud[j] = stemp;
			}
	for (i = 0; i < nst; i++)
	{
		if (mstud[i].sb > srb) {
			cout << mstud[i].fio << " "
				<< mstud[i].sb << endl;
		}
	}
	cout << srb << " sredniy ball";
	return 0;
}