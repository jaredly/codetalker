
// Display the size of a file in C

#include <stdio.h>
#include <io.h>
#include <fcntl.h>
#include <sys\stat.h> 
int main()
{
int fp;

long file_size;

if ((fp = open("f:/cprojects/urls.txt", O_RDONLY)) == -1)
printf("Error opening the file \n");
else
{
file_size = filelength(file_handle);
printf("The file size in bytes is %ld\n", file_size);
close(fp);
}
return 0;
}
