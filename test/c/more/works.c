
#include <stdio.h>

static void times2( int n, int *m ) {
	*m = (2*n);
}

int main( int argc, char *argv[] ) {

	int x, y;
	x = 3;
	y = 4;
	times2( x, &y );

	printf( "x = %d, y = %d\n", x, y );
}

