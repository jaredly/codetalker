
// Earth years to other planets conversion

#include <stdio.h> 
int main(void)
{
float earth;
float mercury,venus,mars,jupiter;
float saturn,uranus,neptune,pluto;
printf("Please enter the amount of earth years to convert.\n");
scanf("%f",&earth);

/*conversions*/
mercury = earth * 365 / 88;
venus = earth * 365 / 225;
mars = earth * 365 / 687;
jupiter = earth / 11.86;
saturn = earth / 29.46;
uranus = earth / 84;
neptune = earth / 164.8;
pluto = earth / 247.7;

/*display conversions*/
printf("Equivalent mercury years is : %f\n",mercury);
printf("Equivalent venus years is : %f\n",venus);
printf("Equivalent mars years is : %f\n",mars);
printf("Equivalent jupiter years is : %f\n",jupiter);
printf("Equivalent saturn years is : %f\n",saturn);
printf("Equivalent uranus years is : %f\n",uranus);
printf("Equivalent neptune years is : %f\n",neptune);
printf("Equivalent pluto years is : %f\n",pluto);

return 0;
}
