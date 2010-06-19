
// Basic example showing constants usage in C

#include <stdio.h>
/*constants for bonus rates and sales*/
#define BONUSRATE1 0.1
#define BONUSRATE2 0.15
#define BONUSRATE3 0.2
#define SALES1 2000
#define SALES2 5000
#define SALES3 10000 
int main()
{
int sales;
double commission;
/*get employees sales*/
printf("Please enter your total sales to the nearest dollar.\n");
scanf("%d", &sales);
/*calculate employees bonus based on info*/
if(sales <=2000)
{
commission = sales * BONUSRATE1;
printf("%g\n" , commission);
}
else if(sales > 2000 && sales <=5000)
{
commission = sales * BONUSRATE2;
printf("%g\n" , commission);
}
else
{
commission = sales * BONUSRATE3;
printf("%g\n" , commission);
}

return 0;
}
