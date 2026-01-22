#include <iostream>
using namespace std;
int main() {
	char s[100];
	char k[100];
	int e = 0;
	cin.getline(s,100); 
	int mlen = 0;
	int mpos = 0;
	int curlen = 0;
	int curpos = 0;
	for (int i = 0; i < strlen(s); i++) {
		if (i == strlen(s) - 1 && s[i]!=' ') {
			if (curlen + 1 > mlen) {
				mlen = curlen + 1;
				mpos = curpos;
			}
		}
		else if (s[i] == ' ' || s[i] == '\n' ) {
			if (curlen > mlen) {
				mlen = curlen;
				mpos = curpos;
			}
			curlen = -1;
			curpos=i+1;
		}
		curlen++;
		if ((s[i] == 'A' || s[i] == 'a') && (s[i - 1] == ' ' || i == 0))
		{
			int d = i;
			while (s[d] != ' ' )
			{
				k[e] = s[d];
				d++;
				e++;
			} 
			k[e] = ' ';
			e++;
		}
	}
	for (int i = 0; i < e; i++) {
		cout << k[i];
	}
	cout << strlen(k) << ' ' << e << ' ';

	cout << "Dlina max slova " << mlen << " Posicia " << mpos+1;
	return 0;
}


