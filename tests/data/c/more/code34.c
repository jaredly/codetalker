
// This checks whether the floppy disk is ready in DOS

#include <stdio.h>
#include <bios.h> 
void main(void)
{
char buffer[8192];

// Try reading head 1, track 1, sector 1
if (biosdisk(2, 0, 1, 1, 1, 1, buffer))
printf("Error accessing drive\n");
else
printf("Drive ready\n");
}
