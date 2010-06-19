
// Create a php file

#include <stdio.h>
#include <conio.h>
#include <io.h>
#include <sys/stat.h> 
int main()
{
int filehandle;
char filename[20];
char countername[20];
int count;
FILE *fp;
printf("Please enter the name of the file you wish to create\n");
printf("in the format myfile.php : \n");
gets(filename);
printf("Now enter a name for the counter file.\n");
gets(countername);
printf("Please enter the starting count.\n");
scanf("%d",&count);

/*create counterfile with the starting count*/
filehandle = creat(countername,S_IREAD|S_IWRITE);
if(fp = fopen(countername,"a"))
{
fprintf(fp,"%d",count); 
fclose(fp);
}
else
printf("cannot open %s ",countername);


/*create php file*/
filehandle = creat(filename,S_IREAD|S_IWRITE);
/*create counter in php file*/
if(fp = fopen(filename,"w+"))
{
fprintf(fp,"<?php\n");
fprintf(fp,"$counterFile = \"%s\";\n",countername);
fprintf(fp,"$line = file($counterFile);\n");
fprintf(fp,"$line[0] ++ ;\n");
fprintf(fp,"$fp = fopen($counterFile ,\"w\");\n");
fprintf(fp,"fputs($fp, \"$line[0]\");\n");
fprintf(fp,"fclose($fp);\n");
fprintf(fp,"echo $line[0];\n");
fprintf(fp,"?>\n");
fclose(fp);
}
else
printf("cannot create %s",filename);
return 0;
}
