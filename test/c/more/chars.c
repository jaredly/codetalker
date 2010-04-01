#include <stdio.h>
/* cntrl d terminates */
int main( int argc, char *argv[] ) {
	int c;
	while( ( c = getchar() ) != EOF ) {
		putchar( c );
	}   
}

