
// Blinking Lights on Keyboard

#include<dos.h>
void interrupt mytimer();
void interrupt (*prev)();
int run=0,lt=0,ticks=0;
char far *mode;
int temp;
void main()
{
mode=(char far*)0x417;
prev=getvect(0x8);
setvect(0x8,mytimer);
keep(0,100);
getch();
}
void interrupt mytimer()
{
if(run==0)
{
ticks++;
if(ticks==5)
{
ticks=0;
run=1;
lt++;
if(lt==1)
{
temp=*mode;
temp=temp&0x8f;
temp=temp|0x40;
*mode=temp;
}
else if(lt==2)
{
temp=*mode;
temp=temp&0x8f;
temp=temp|0x20;
*mode=temp;
}
else if(lt==3)
{
temp=*mode;
temp=temp&0x8f;
temp=temp|0x10;
*mode=temp;
lt=0;
}
}
run=0;
}
(*prev)();
}
