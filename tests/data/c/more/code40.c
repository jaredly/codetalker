
// Math co-processor

#include <stdio.h>
#include <dos.h>
#include <stdlib.h>
#include <bios.h> 
int main(void)
{
unsigned result;

clrscr();
result = biosequip();
if(result & 0x0002)
printf("Math co-processor installed\n");
else
printf("Math co-processor is not installed.\n");

return 0;

}
