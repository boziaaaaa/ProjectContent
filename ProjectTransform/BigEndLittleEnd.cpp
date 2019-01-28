// test9.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
//#include <fstream>
//#include<iostream>
using namespace std;

void ExchangeFloat(unsigned char* pData);
void BigEndLittleEnd(float* LatLonArray,int Height,int Width)
{
	//std::ifstream fin("D:\\FY2E_Data\\LatLon\\FY2D_IJToLatLon.NOM", std::ios::binary);
	//float *LatLonArray = new float[2288*2288];
	float temp = 0;
	//fin.read((char*)LatLonArray, sizeof(float)*2288*2288);
	//std::cout << "int = " << temp << std::endl;
	for(int i = 0;i<Height * Width;i++)
	{
		    temp = LatLonArray[i];
			//std::cout << "int = " << temp << std::endl;
			ExchangeDouble((unsigned char *)&temp);
			LatLonArray[i] = temp;
			/*if(temp!=300)
			{
			  std::cout << "int = " << temp << std::endl;
			}*/
	}
	return 0;
}

void ExchangeFloat(unsigned char* pData)
{	
	unsigned char bSave;
	bSave    = pData[0];
	pData[0] = pData[3];
	pData[3] = bSave;
	bSave    = pData[1];
	pData[1] = pData[2];
	pData[2] = bSave;
}