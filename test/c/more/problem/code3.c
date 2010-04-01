
// Adds text to current dislay line while person is typing and increases
// the cursor position

#include<dos.h>
void interrupt our();
void interrupt (*prev)();
void writechar(char ch,int row,int col,int attr);
int a,b,kp,run=0;
char far *scr;
void main()
{
scr=(char far*) 0xb8000000;
prev=getvect(9);
setvect(9,our);
keep(0,500);
}
void interrupt our()
{
kp++;
if(kp==5)
{
run++;
_AH=3;
_BH=0;
geninterrupt(0x10);
a=_DH;
b=_DL;
if(run==1)
writechar('M',a,b,7);
if(run==2)
writechar('S',a,b,7);
if(run==3)
{
writechar('P',a,b,7);
run=0;
}
b++;
_AH=2;
_BH=0;
_DH=a;
_DL=b;
geninterrupt(0x10);
kp=0;
}
(*prev)();
}
void writechar(char ch,int row,int col,int attr)
{
*(scr+row*160+col*2)=ch;
*(scr+row*160+col*2+1)=attr;
}
