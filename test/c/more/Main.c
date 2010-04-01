/*
 *	This is the main program source file.
 *
 *	It *must* include the ".h" files for each module that it uses.
 *
 */

#include "Module1.h"
#include "Module2.h"

extern int main( int argc, char *argv[] ) {

	char *p = "Hello, world.\n";

	m1_Function( p );
	m2_Function( p );
	
	return( 0 );
}


