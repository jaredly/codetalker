
// Average example

// This program calculates an average of the numbers entered

#include <stdio.h> 
int Average(int i);

int main()
{
int num;
do{

printf("Enter numbers ( -1 to quit ).\n");
scanf("%d",&num);
/*if number is not -1 print the average*/
if(num != -1)
printf("The average is %d", Average(num));
printf("\n");

}while(num>-1);

return 0;
}

int Average(int i)
{
static int sum = 0, count = 0; 
sum = sum + i; 
count++; 
return sum / count; 
}
