/*
 *	This is the Module1 source file.
 *
 *	It *should* include its own ".h" file.
 *
 */

#include <stdio.h>
#include "Module1.h"

extern void m1_Function( char *p ) {

	printf( "%.7s m1_function ", p );
}


