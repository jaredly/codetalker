
// Display free disk space in DOS systems

#include <stdio.h>
#include <dos.h> 
void main(void)
{
struct dfree diskinfo;
long disk_space;

getdfree(3, &diskinfo);
disk_space = (long) diskinfo.df_avail * (long) diskinfo.df_bsec * (long) diskinfo.df_sclus;

printf("Available disk space %ld\n", disk_space);
}
