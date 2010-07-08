
// Delay for 5 seconds example

#include <stdio.h>
#include <time.h> 
int main()
{
time_t start;
time_t current;

time(&start);
printf("delay for 5 seconds.\n");
do{
time(&current);
}while(difftime(current,start) < 5.0);
printf("Finished delay.\n");


return 0;
}
