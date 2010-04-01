
#include <stdio.h>

int main( int argc, char *argv[] ) {

	int *p;

	p = (int *) malloc( sizeof( int ) );

	(*p) = 100;
	(*p)++;
	(*p) *= 5;

	printf( "%p\n", &p );

	printf( "p = %p, *p = %d (hex=%x,oct=%o)\n", p, *p, *p, *p );

	printf( "Ooops: %d\n", p );
	printf( "Hex:   %x\n", p );
}

