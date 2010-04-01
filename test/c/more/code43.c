
// Mirror your DOS screen

#include"dos.h"
void interrupt (*prevtimer)();
void interrupt mytimer();
void writechar(char ch,int row,int col,int attr);
int ticks=0;
int running=0;
unsigned long far *time=(unsigned long far*) 0x46c;
char far* scr;
char far* mode;
void main()
{
if((*mode &0x30)== 0x30)
scr=(char far*) 0xb0000000;
else
scr=(char far*) 0xb8000000;
prevtimer=getvect(8);
setvect(8,mytimer);
keep(0,1000);
}
void interrupt mytimer()
{
int i,j,k;
char t[80];
ticks++;
if(ticks==18)
{
ticks=0;
if(running==0)
{
running=1;
}
for(i=0;i<25;i++)
{
for(k=0;k<=79;k++)
{
t[k]=*(scr+i*160+k*2);
}
k=0;
for(j=79;j>=0;j--)
{
writechar(t[k],i,j,7);
k++;
}
}
}
running=0;
(*prevtimer)();
}
void writechar(char ch,int row,int col,int attr)
{
*(scr+row*160+col*2)=ch;
*(scr+row*160+col*2+1)=attr;
}
