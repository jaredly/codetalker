
// Displays the attributes of a selected file

#include <stdio.h>
#include <io.h> 
int main()
{
int mode;
/*check a files attributes*/
mode = access("f:/samples.txt",0);
if(mode)
printf("File does not exist.\n");
else
/*check if the file can be written to*/
mode = access("f:/samples.txt",2);
if(mode)
printf("File cannot be written.\n");
else
printf("file can be written to.\n");

/*check if file can be read*/
mode = access("f:/samples.txt",4);
if(mode)
printf("File cannot be read.\n");
else
printf("File can be read.\n");

/*check if afile can be read/written*/
mode = access("f:/samples.txt",6);
if(mode)
printf("File cannot be read/written to.\n");
else
printf("File can be read/written to.\n");

return 0;
}
