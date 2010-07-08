
// Display whether a number is odd or even

#include <stdio.h> 
int main()
{
int number ;
printf("Enter a whole number\n");
scanf("%d",&number);
if(number % 2 == 0)
printf("Your number is even.\n");
else
printf("Your number is odd.\n");

return 0;
}
