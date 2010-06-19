
// File functions

// Open a file, read a file and write to a file
#include <stdio.h> 
int main()
{
float sales , commission;
FILE *fin, *fout;
fin = fopen("d:\\sales.dat","r");
fout = fopen("d:\\commission.dat","w");
while (fscanf(fin,"%f",&sales) != EOF)
{
fprintf(fout,"Your sales for the year were %8.2f \n",sales);
if(sales < 30000)
commission = sales / 100 * 5;
else
commission = sales / 100 * 10;
fprintf(fout,"Your commission is %8.2f",commission);
}
return 0;
}
