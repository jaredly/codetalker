
// A simple dice throwing example

#include <stdlib.h>
#include <stdio.h>
#include <time.h> 
 

void main()
{
/*variables*/
int mydice1 ,mydice2 ,yourdice1 ,yourdice2,myresult,yourresult ;
/*seed the random number generator*/
srand((unsigned)time(NULL));
printf("Lets play a game.\n");
printf("The highest score of the two dice wins\n");
/*get a random number from 1 to 6*/
mydice1 = rand() % 6 + 1;
printf("My first throw is %i\n",mydice1);
/*get a random number from 1 to 6*/
mydice2 = rand() % 6 + 1;
printf("My second throw is %i\n",mydice2);
printf("Your turn now.\n");
/*get a random number from 1 to 6*/
yourdice1 = rand() % 6 + 1;
printf("Your first throw is %i\n",yourdice1);
/*get a random number from 1 to 6*/
yourdice2 = rand() % 6 + 1;
printf("Your second throw is %i\n",yourdice2);
/*calculate the total of the two throws*/
myresult = mydice1 + mydice2; 
yourresult = yourdice1 + yourdice2;
/*display the result*/
printf("I scored %i , you scored %i\n",myresult,yourresult);
if (myresult > yourresult)
printf("I win , better luck next time.\n");
else if(myresult < yourresult)
printf("You win , you were lucky that time.\n");
else
printf("Its a tie.\n");

printf("\n");
}
