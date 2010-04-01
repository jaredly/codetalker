
// Random numbers in a range

#include <stdlib.h>
#include <stdio.h>
#include <time.h> 
 
void main()
{
int x ;
srand((unsigned)time(NULL));

for(x=0;x<=100;x++)
printf("%i\t",rand()%10 + 1);

}
