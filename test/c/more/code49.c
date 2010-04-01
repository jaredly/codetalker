
// Reboot a PC , probably DOS

#include<dos.h>
#define reboot 0x19
void rebootpc()

{
union REGS inregs,outregs;
int86(reboot, &inregs, &outregs); // Call BIOS
}
void main()


{
rebootpc();
}
