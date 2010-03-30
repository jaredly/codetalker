#include <stdio.h>


int main (int argc, const char * argv[]) {
     
     int numToPrint, i;
     double num1, num2, ans;
     
     num1 = 0;
     num2 = 1;
     
     printf("How many numbers would you like to print?\t");
     scanf("%d", &numToPrint);
     
     printf("1\t%.0f\n2\t%.0lf\n", num1, num2);
     
     for(i = 0; i < (numToPrint - 2); ++i){
          
          ans = (num1 + num2);
          
          printf("%d\t%.0lf\n", i+3, ans);
          
          num1 = num2;
          num2 = ans;
     }
     
     
    return 0;
}
