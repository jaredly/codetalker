
// Earth to Martian Years conversion

#include <stdio.h> 
int main(void)
{
float earth_years , martian_years;
printf("Please enter the amount of earth years to convert.\n");
scanf("%f",&earth_years);

martian_years = earth_years * 365 / 687;
printf("Equivalent martian years is : %f\n",martian_years);
return 0;
}
