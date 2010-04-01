#include <stdio.h>

int main( int argc, char *argv[] ) {
	int i;

	printf("\nThe zeroth arguement ie argv[0] is interesting %s\n\n", argv[0]);
	printf( "Number of arguments = %d\n", argc-1 );
	for( i=1; i<argc; i++ )
		printf( "   Argument %d = %s\n", i, argv[ i ] );
}

