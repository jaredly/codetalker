
// Colored menu in C

#include <conio.h>

int menu(void);
void setcolor(unsigned short color);


main()
{
while(1)
{
/*get selection and execute the relevant statement*/
switch(menu())
{
case 1:
{
setcolor(8);
puts("You selected menu item 1\n");
puts("Finished item 1 task\n");
break;
}
case 2:
{ 
setcolor(11);
puts("You selected menu item 2\n");
puts("Finished item 2 task\n");
break;
}
case 3:
{
setcolor(12);
puts("You are quitting\n"); 
exit(0);
break;
}
default:
{
puts("Invalid menu choice\n");
break;
}
}
}
return 0;
}

void setcolor(unsigned short color)
{
HANDLE hcon = GetStdHandle(STD_OUTPUT_HANDLE);
SetConsoleTextAttribute(hcon,color);
}
/*menu function*/
int menu(void)
{
int reply;
/*display menu options*/
setcolor(6);
puts("Enter 1 for task 1.\n");
setcolor(9);
puts("Enter 2 for task 2.\n");
setcolor(2);
puts("Enter 3 to quit.\n");
/*scan for user entry*/
scanf("%d", &reply);

return reply;
}
