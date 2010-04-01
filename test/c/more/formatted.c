#include <stdio.h>

int main( int argc, char *argv[] ) {

	int i;
	double d;
	char s[256];

	scanf( "%d, %lf\n", &i, &d );
	printf( "i = %d, f = %f\n", i, d );
	scanf( "%d, %s\n", &i, s );
	printf( "i = %d, s = %s\n", i, s );
}

