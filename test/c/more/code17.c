
// count occurrences of values in an array

#include <stdio.h> 
void print_arr(int grades[], int elements);
int count_passes(int grades[], int elements,int value);

int main(void)
{
int grades[10] = {70,80,95,65,35,85,54,78,45,68};
int result;
print_arr(grades,10);
result = count_passes(grades,10,70);
if(result == 1)
printf("There was %d pass.\n",result);
else
printf("There were %d passes.\n",result);
return 0;
}

void print_arr(int grades[], int elements)
{
int i;

for(i = 0;i < elements;i++)
{
printf("%d ",grades[i]);
}
printf("\n");
}

int count_passes(int grades[], int elements,int value)
{
int i ,passes = 0 ;
for(i = 0;i < elements;i++)
{
if(grades[i] >= value)
passes++;
}
return(passes);
}
