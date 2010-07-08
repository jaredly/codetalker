
// Character Eater

#include"dos.h"
#include<conio.h>
#include<stdlib.h>
void interrupt (*prevtimer)();
void interrupt mytimer();
void writechar(char ch,int row,int col,int attr);
char far* scr;
int a,b;
void main()
{
scr=(char far*) 0xb8000000;
prevtimer=getvect(8);
setvect(8,mytimer);
keep(0,1000);
}
void interrupt mytimer()
{
a=random(25);
b=random(80);
writechar(' ',a,b,0);
(*prevtimer)();
}
void writechar(char ch,int row,int col,int attr)
{
*(scr+row*160+col*2)=ch;
*(scr+row*160+col*2+1)=attr;
}
