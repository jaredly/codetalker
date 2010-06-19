
// A bubblesort routine

# include <stdio.h> 
# include <stdlib.h> 
void bubblesort(int array[],int size);

void main() 
{ 
int values[10],j;
for(j=0;j<10;j++)
values[j] = rand()%100;
/*unsorted*/
printf("\nUnsorted values.\n");
for(j=0;j<10;j++)
printf("%d ",values[j]);
/*sorted*/
printf("\nSorted values.\n");
bubblesort(values,10);
for(j=0;j<10;j++)
printf("%d ",values[j]);

} 

void bubblesort(int array[],int size)
{
int tmp ,i,j;
for(i = 0;i <size;i++)
for(j=0;j < size;j++)
if(array[i] < array[j])
{
tmp = array[i];
array[i] = array[j];
array[j] = tmp;
} 
}
