
// Ohms law example

#include <stdio.h>
#include <conio.h>
#include <stdlib.h> 
int main()
{
char ch;
float voltage , current , resistance , result;
printf("Ohms law calculator.\n");
printf("Please choose from following calculcations.\n");
printf("1. choose 1 to calculate the voltage.\n");
printf("2. choose 2 to calculate the current.\n");
printf("3. choose 3 to calculate the resistance.\n");
printf("Anything else to quit.\n");

scanf("%c",&ch);
switch(ch)
{
case '1' :
printf("please enter the current in amps.\n");
scanf("%f",&current);
printf("Now enter the resistance in ohms.\n");
scanf("%f",&resistance);
result = current * resistance;
printf("The voltage is %0.2f volts.\n",result);
break;
case '2' :
printf("please enter the voltage in volts.\n");
scanf("%f",&voltage);
printf("Now enter the resistance in ohms.\n");
scanf("%f",&resistance);
result = voltage / resistance;
printf("The current is %0.2f amps.\n",result);
break;
case '3' :
printf("please enter the voltage in volts.\n");
scanf("%f",&voltage);
printf("Now enter the current in amps.\n");
scanf("%f",&current);
result = voltage / current;
printf("The resistance is %0.2f ohms.\n",result);
break;
default :
exit(0);
break;

}
return 0;
}
