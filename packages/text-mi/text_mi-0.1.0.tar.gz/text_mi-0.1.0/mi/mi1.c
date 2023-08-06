#include "mi1.h"

double logarithm(double a)
{
	if (a != 0)
	{
		return log2(a);
	}
	else
	{
		return 0;
	}
}

long double mi(char** news, unsigned n2, char* class_, char** classes, char* word)
{
	long double N11 = 0;
	long double N10 = 0;
	long double N01 = 0;
	long double N00 = 0;
	for(unsigned j = 0; j < n2; j++)
	{
		if(strstr(classes[j], class_) != NULL)
		{
			if(strstr(news[j], word) != NULL) 
			{
				N11 ++;
			}
			else 
			{
				N01 ++;
			}
		}
		else 
		{
			if(strstr(news[j], word) != NULL) 
			{
				N10 ++;
			}
			else 
			{
				N00 ++;
			}
		}
	}
	long double N = N11+N10+N00+N01;
	long double N1x = N11+N10;
	long double Nx1 = N11 + N01;
	long double N0x = N01+N00;
	long double Nx0 = N10 + N00;

	long double result = 0;
	if (N1x*Nx1 > 0) {
		result += (N11/N)*logarithm((N*N11)/(N1x*Nx1));
	}
	if (N0x*Nx1 > 0) {
		result += (N01/N) * logarithm((N*N01)/(N0x*Nx1));
	}
	if (N1x*Nx0 > 0) {
		result += (N10/N) * logarithm((N*N10)/(N1x*Nx0));
	}
	if (N0x*Nx0 > 0) {
		result += (N00/N) * logarithm((N*N00)/(N0x*Nx0));
	}
	return result;
}
