
// Display todays date

#include <stdio.h>
#include <dos.h>
#include <stdlib.h>
#include <bios.h> 
int main(void)
{
struct date DATE;

clrscr();
getdate(&DATE);
printf("The year is : %d\n",DATE.da_year);
printf("The month is : %d\n",DATE.da_month);
printf("The day is : %d\n",DATE.da_day);

return 0;

}
