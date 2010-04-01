
// Disk diagnostics in DOS, compiled with Turbo C

#include <stdio.h>
#include <dos.h>
#include <stdlib.h>
#include <bios.h> 
int main(void)
{

int status;
int command = 19;
int drive = 0;
int head = 0;
int track = 1;
int sector = 1;
int nosectors = 1;
char buffer[512];

clrscr();
status = biosdisk(command,drive,head,track,sector,nosectors,buffer);
if(status == 0)
printf("Diagnostics.\n");
else
printf("Unable to run diagnostics.\n");
return 0;

}
