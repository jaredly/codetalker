
// Area of circle

// Calculates the area of a circle

#include <stdio.h> 
#define PI 3.14159

int main()
{
float sum , radius ;
printf("This program works out the area of a circle.\n");
printf("Enter the radius of the circle.\n");
scanf("%f",&radius);
/*area of a circle is pi * radius * radius*/
sum = PI * radius * radius;
/*display the area*/
printf("The area of a circle is %f.\n",sum);
return 0;
}
