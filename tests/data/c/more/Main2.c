/*
 *   Main2.c
 *   3 Source File Example for SEng265
 *   Written by Glen Darling.
 */


#include <stdio.h>
#include <stdlib.h>


/* MUST include this to use List functions */
#include "List2.h" 


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
    DigitList x;

    srand( (unsigned int) getpid() );

    list_New( &x );

    /* Zero the frequency array */
    for( i=0; i<10; i++ )
        n[i] = 0;

    /* Insert digits, counting frequency as we go */
    for( i=0; i<1000; i++ ) {
        r = RandomNumberInRange( 0, 9 );
        n[r]++;
        list_Add( &x, r );
    }

    /* Display frequencies */
    for( i=0; i<10; i++ )
        printf( "%d: %d\n", i, n[i] );

#if kDEBUG
    /* Display raw data if we are debugging */
    for( i=1; i<=list_Size( x ); i++ )
        printf( "%u ", list_Nth( x, i ) );
    printf( "\n" );
#endif

    /* Zero the frequency array */
    for( i=0; i<10; i++ )
        n[i] = 0;

    /* Recompute the frequencies by traversing the list */
    for( i=1; i<=list_Size( x ); i++ )
        n[ list_Nth( x, i ) ]++;

    /* Display frequencies again */
    for( i=0; i<10; i++ )
        printf( "%d: %d\n", i, n[i] );

    printf( "\n" );
    list_Dispose( &x );

    return( 0 );
}