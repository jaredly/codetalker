#include <stdio.h>
// one comment
/*another o * one*/
int main()
{
   char* szFirst = "Literal String";
   char* szSecond = "Literal String";

   szFirst[3] = 'q';
   printf("szFirst (%s) is at %d, szSecond (%s) is at %d\n",
         szFirst, szFirst, szSecond, szSecond);

   return 0;
}
