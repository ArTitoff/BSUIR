#pragma once
#include <iostream>
#include <string>
#include <time.h>



using namespace std;

/**@class Piatnashky 
* @brief Class for plaing tag
*/


class Piatnashky {
public:
	int PointX;
	int PointY;
	int Field[4][4];



	 

	void CerateRandomField(); 

	void Print(); 

	void SwapLeft(); 

	void SwapRight(); 

	void SwapUp(); 

	void SwapDown(); 

	void Proverka(int& choice);
 
	void Menu();
	void Menu_2(const int& choice); 

public:
	int& operator[](const int& index); 
	Piatnashky(); 
	void Play();
};