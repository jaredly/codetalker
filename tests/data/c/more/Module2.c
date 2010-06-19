/*
 *	This is the Module2 source file.
 *
 *	It *should* include its own ".h" file.
 *	And it *must* include the ".h" files for each module that it uses.
 *
 */

#include "Module2.h"
#include "Module3.h"

extern void m2_Function( char *p ) {

	m3_Function( p + 7 );
}


