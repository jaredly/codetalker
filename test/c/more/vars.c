#include <stdio.h>

int i,j,k;
float x;
char ch;
int main( int argc, char *argv[] )
{
	printf( "Hello, world.\n" );
	i = 5;
	x=2.0;
	ch = 'A';
	
	printf("\nordinary exercise...\n\n");
	printf("print i %d \n",i);
	printf("print x %f \n",x);
	printf("print ch %c \n",ch);

	printf("\nwrong formats...\n\n");
	printf("hmmm i %f \n",i);
	printf("hmmm x %d \n",x);
	printf("hmmm ch %d \n",ch);

	printf("\nreferences formatted as addresses...\n\n");
	printf(" where i %p \n",&i);
	printf(" where x %p \n",&x);
	printf(" where ch %p \n",&ch);

	printf("\ndereferencing ...\n\n");
	printf("print i %d \n",*(&i));
	printf("print x %f \n",*(&x));
	printf("print ch %c \n",*(&ch));

	return( 0 );
}
