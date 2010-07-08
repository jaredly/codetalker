
// Circumference of a circle

#include <stdio.h>
#define PI 3.14159 
int main(void)
{
float area , circumference , radius;
printf("What is the radius of the circle.\n");
scanf("%f",&radius);

area = PI * radius * radius;
circumference = 2.0 * PI * radius;

printf("The circumference of the circle is %1.2f.\n",circumference);
printf("The area of the circle is %1.2f.\n",area);

return 0;
}
