
// A power calculator in C

#include <stdio.h> 
int main()
{
float power,voltage,current;
voltage = current = 0;

printf("Power calculator.\n");
printf("This will calculate the power in watts , ");
printf("when you input the voltage and current.");
/*get the voltage*/
printf("Enter the voltage in volts.\n");
scanf("%f",&voltage);
/*get the current*/
printf("Enter the current in amps.\n");
scanf("%f",&current);
/*calculate the power*/
power = voltage * current;
printf("The power in watts is %.2f watts\n",power);

return 0;
}
