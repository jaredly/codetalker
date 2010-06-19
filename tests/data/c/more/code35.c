
// Print to a file using the fprintf function

#include <stdio.h> 
int main()
{
FILE *fp;
int rating = 9;
if (fp = fopen("d:/website.txt", "w"))
{
fprintf(fp, "WWW\n");
fprintf(fp, "Topic: computer programming\n");
fprintf(fp, "Rating out of 10 : %d \n",rating );
fclose(fp);
}
else
printf("Error opening d:/website.txt\n");

return 0;
}
