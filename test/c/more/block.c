
#include <stdio.h>

#define kBUFFER_SIZE 1024

extern void main( int argc, char *argv[] ) {

	FILE *f1, *f2;
	char buffer[ kBUFFER_SIZE ];
	int n;

	f1 = fopen( argv[ 1 ], "r" );
	f2 = fopen( argv[ 2 ], "w" );

	while( ( n = fread( buffer, 1, kBUFFER_SIZE, f1 ) ) > 0 ) {
		fwrite( buffer, 1, n, f2 );
	}   

	fclose( f2 );
	fclose( f1 );

}

