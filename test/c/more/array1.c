//array1.c
// arrays example
#include <stdio.h>

int a1 [] = {16, 2, 77, 40, 13};
int sum = 0;
int n;

int main ()
{
  for (n=0 ; n<5 ; n++ )
  {
    sum += a1[n];
  }
  printf("%d \n", sum);
  return 0;
}

