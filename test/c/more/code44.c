
// Move text in DOS

#include <conio.h>
#include <stdio.h>

int main(void)
{
clrscr();

printf("Here is some text we will move.\n");
printf("Press key to move the text.\n");
getch();
/*parameters are left,top,right,bottom,destleft,desttop*/
movetext(1,1,30,1,1,20);

return 0;

}
