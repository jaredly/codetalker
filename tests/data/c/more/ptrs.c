#include <stdio.h>

int main( int argc, char *argv[] ) {

	short x=12;
	short *p=&x;

	printf( "x: %d\n", x );
	printf( "p: %p\n", p );
	printf( "size of x: %d\n", sizeof(x) );
	printf( "size of p: %d\n", sizeof(p) );



}


