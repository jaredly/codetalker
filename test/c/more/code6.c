
// Beeps the speaker program

#include <dos.h>
#include <stdio.h>
#include <stdlib.h> 
int menu(void);


main()
{
while(1)
{
/*get selection and execute the relevant statement*/
switch(menu())
{
case 1:
{
puts("sound the speaker 1\n");
sound(2000);
sleep(2);
nosound();
break;
}
case 2:
{
puts("sound that speaker 2\n");
sound(4000);
sleep(2);
nosound();
break;
}
case 3:
{
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

/*menu function*/
int menu(void)
{
int reply;
/*display menu options*/
puts("Enter 1 for beep 1.\n");
puts("Enter 2 for beep 2.\n");
puts("Enter 3 to quit.\n");
/*scan for user entry*/
scanf("%d", &reply);

return reply;
}
