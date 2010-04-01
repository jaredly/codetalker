/*
 *
 *   Example list c the whole banana
 *
 */


#include <stdio.h>     // for printf()
#include <time.h>      // for clock()
#include <stdlib.h>    // for malloc(), free(), srand(), and rand()


#define kDEBUG 0


/* Define some data types */

   typedef unsigned short Digit;

   typedef struct DigitList {
      struct DigitListNode *List;
   } DigitList;

   typedef struct DigitListNode {
      Digit Data;
      struct DigitListNode *Next;
   } DigitListNode, *DigitListNodePtr;


/* Function prototypes */

   static short RandomNumberInRange( short min, short max );
   static void list_New( DigitList *pList );
   static void list_Dispose( DigitList *pList );
   static void list_Add( DigitList *pList, Digit digit );
   static short list_Size( DigitList list );
   static Digit list_Nth( DigitList list, short n );


/* List functions */

static void list_New( DigitList *pList ) {

	( pList->List ) = NULL;
}

static void list_Dispose( DigitList *pList ) {

	DigitListNodePtr p;

	p = ( pList->List );
	while( p != NULL ) {
		( pList->List ) = p->Next;
		free( p );
		p = ( pList->List );
	}
	pList->List = NULL;
}

static short list_Size( DigitList list ) {

	short result;
	DigitListNodePtr p;

	p = ( list.List );
	result = 0;
	while( p != NULL ) {
		p = ( p->Next );
		result++;
	}

	return( result );
}

static Digit list_Nth( DigitList list, short n ) {

	DigitListNodePtr p;

	p = ( list.List );
	while( p != NULL ) {
		n--;
		if( !n )
			return( p->Data );
		p = ( p->Next );
	}
}

static void list_Add( DigitList *pList, Digit digit ) {

	DigitListNodePtr out;

	out = (DigitListNodePtr) malloc( sizeof( DigitListNode ) );
	out->Data = digit;
	out->Next = pList->List;
	pList->List = out;
}


/* List testing functions */

static short RandomNumberInRange( short min, short max ) {
	return( min+(short)(((double)(1+max-min))*((double)rand())/(1.0+((double)RAND_MAX))) );
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



