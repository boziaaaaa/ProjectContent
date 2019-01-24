#include<stdio.h>
#include<iostream>
using namespace std;
extern "C" int c()
{
cout<<"I am C++"<<endl;

return 0;
}

extern "C" int add(int a,int b)
{
int c = a + b;
return c;
}

extern "C" int Switch(int* a,int* b)
{
int* c;
*c = *a;
*a = *b;
*b = *c;
//*a = 999;
cout<<"--> "<<*a<<*b<<endl;
return 0;
}
