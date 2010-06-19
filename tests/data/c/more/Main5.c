/*
 *   Main5.c
 *   Almost OO Example for SEng265
 *   Written by Glen Darling.
 */


#include <stdio.h>
#include <stdlib.h>


#include "List5.h"


#define kDEBUG 0


/* List testing functions */

static short RandomNumberInRange( short min, short max ) {
    return( min +
        (short)(((double)(1+max-min))*((double)rand())/
        (1.0+((double)RAND_MAX))) );
}


/* Main function */

int main( int argc, char *argv[] ) {

    short i, n[10];
    Digit r;
    DigitList *p;

    srand( (unsigned int) getpid() );

    p = list_New();

    /* Zero the frequency array */
    for( i=0; i<10; i++ )
        n[i] = 0;

    /* Insert digits, counting frequency as we go */
    for( i=0; i<1000; i++ ) {
        r = RandomNumberInRange( 0, 9 );
        n[r]++;
        if( ! list_Add( p, r ) ) {
            printf( "Out of memory adding element number %d.\n", i );
            exit( 1 );
        }
    }

    /* Display frequencies */
    for( i=0; i<10; i++ )
        printf( "%d: %d\n", i, n[i] );

#if kDEBUG
    /* Display raw data if we are debugging */
    for( i=1; i<=list_Size( *p ); i++ )
        printf( "%u ", list_Nth( *p, i ) );
    printf( "\n" );
#endif

    /* Zero the frequency array */
    for( i=0; i<10; i++ )
        n[i] = 0;

    /* Recompute the frequencies by traversing the list */
    for( i=1; i<=list_Size( *p ); i++ )
        n[ list_Nth( *p, i ) ]++;

    /* Display frequencies again */
    for( i=0; i<10; i++ )
        printf( "%d: %d\n", i, n[i] );

    printf( "\n" );
    list_Dispose( &p );

    return( 0 );
}
