#include <stdio.h>

int main( int argc, char *argv[] ) {

	FILE *f1, *f2;
	int c;

	f1 = fopen( argv[ 1 ], "r" );
	f2 = fopen( argv[ 2 ], "w" );

	while( ( c = getc( f1 ) ) != EOF ) {
		putc( c, f2 );
	}   

	fclose( f2 );
	fclose( f1 );

}

