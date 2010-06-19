
// Blinking text in DOS, compiled with Turbo C

#include <conio.h> 
int main()
{
int color;
textattr(128 + 10);
cprintf("This is blinking text\n");
return 0;
}
