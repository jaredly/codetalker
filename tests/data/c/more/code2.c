
// Abswrite example , compiled with Turbo C

#include <stdio.h>
#include <dos.h>
#include <stdlib.h>
#include <bios.h> 
int main(void)
{
unsigned char buffer[512];

clrscr();
printf("Insert a blank disk in the A: drive , then press any key.\n");
/*wait for keypress*/
getch();
if(abswrite(0,1,1,&buffer) != 0)
printf("Cannot write to the A drive.\n");
else
printf("Drive A , Sector 1 written to\n");

return 0;

}
