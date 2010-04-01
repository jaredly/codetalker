
// Convert MB to KB

#include <stdio.h> 
int main(void)
{
double megabytes , kilobytes;
printf("Please enter the amount of megabytes to convert.\n");
scanf("%Lf",&megabytes);
/*convert megabytes to kilobytes*/
kilobytes = megabytes * 1024;
/*convert kilobytes to megabytes*/
/*this is for kilobytes to megabytes*/
/*megabytes = kilobytes / 1024*/
printf("There are %Lf kilobytes in %Lf megabytes.\n",kilobytes,megabytes);

return 0;
}
