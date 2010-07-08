
// Search an array

#include <stdio.h> 
void print_arr(int myArray[], int elements);
int search_arr(int myArray[], int elements, int number);

int main(void)
{
int myArray[10] = {12,23,56,35,18,65,12,87,73,9};
int result,number;
print_arr(myArray,10);
number = 65;
result = search_arr(myArray,10,number);
if(result == -1)
printf("%d was not found.\n",number);
else
printf("Found %d\n",result);
return 0;
}

void print_arr(int myArray[], int elements)
{
int i;

for(i = 0;i < elements;i++)
{
printf("%d ",myArray[i]);
}
printf("\n");
}

int search_arr(int myArray[], int elements, int number)
{
int i;
for(i = 0;i < elements;i++)
{
if(myArray[i] == number)
return(number);
}
return(-1);
}
