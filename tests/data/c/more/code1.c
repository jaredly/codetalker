
// Absread in C

Th// is reads individual disk sectors , compiled with Turbo C

#include <stdio.h>
#include <dos.h>
#include <stdlib.h>
#include <bios.h> 
int main(void)
{
unsigned char buffer[512];

clrscr();
printf("Insert disk in the A: drive , then press any key.\n");
/*wait for keypress*/
getch();
if(absread(0,1,1,&buffer) != 0)
printf("Cannot read the A drive.\n");
else
printf("Drive A , Sector 1 read\n");

return 0;

}
