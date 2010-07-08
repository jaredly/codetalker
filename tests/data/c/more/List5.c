/*
 *   List5.c
 *   Almost OO Example for SEng265
 *   Written by Glen Darling.
 */


#include <stdio.h>
#include <stdlib.h>
#include <assert.h>


#include "List5.h"


#define kCheckDigitList         "DigitList"
#define kCheckDigitListNode  "DigitListNode"


/* List functions */

extern DigitList *list_New() {
    DigitList *pList;
    pList = (DigitList *) malloc( sizeof( DigitList ) );
    if( pList != NULL ) {
        ( pList->Check ) = kCheckDigitList;
        ( pList->List ) = NULL;
    }
    return( pList );
}

extern int list_Add( DigitList *pList, Digit digit ) {
    DigitListNodePtr out;
    assert( pList != NULL );
    assert( digit >=0 && digit <= 9 );
    assert( !strcmp( pList->Check, kCheckDigitList ) );
    out = (DigitListNodePtr) malloc( sizeof( DigitListNode ) );
    if( out != NULL ) {
        out->Check = kCheckDigitListNode;
        out->Data = digit;
        out->Next = pList->List;
        pList->List = out;
        return( 1 );
    }
    return( 0 );
}

extern short list_Size( DigitList list ) {
    short result;
    DigitListNodePtr p;
    assert( !strcmp( list.Check, kCheckDigitList ) );
    p = ( list.List );
    result = 0;
    while( p != NULL ) {
        assert( !strcmp( p->Check, kCheckDigitListNode ) );
        assert( p->Data >=0 && p->Data <= 9 );
        p = ( p->Next );
        result++;
    }
    return( result );
}

extern Digit list_Nth( DigitList list, short n ) {
    DigitListNodePtr p;
    assert( !strcmp( list.Check, kCheckDigitList ) );
    p = ( list.List );
    while( p != NULL ) {
        assert( !strcmp( p->Check, kCheckDigitListNode ) );
        assert( p->Data >=0 && p->Data <= 9 );
        n--;
        if( !n )
            return( p->Data );
        p = ( p->Next );
    }
    assert( 0 );
    return( -1 );  /* This statement is not reached */
}

extern void list_Dispose( DigitList **ppList ) {
    DigitListNodePtr p;
    assert( ppList != NULL );
    assert( (*ppList) != NULL );
    assert( !strcmp( (*ppList)->Check, kCheckDigitList ) );
    p = ( (*ppList)->List );
    while( p != NULL ) {
        assert( !strcmp( p->Check, kCheckDigitListNode ) );
        assert( p->Data >=0 && p->Data <= 9 );
        ( (*ppList)->List ) = p->Next;
        p->Check = NULL;
        p->Data = -1;
        p->Next = NULL;
        free( p );
        p = ( (*ppList)->List );
    }
    (*ppList)->Check = NULL;
    (*ppList)->List = NULL;
    free(*ppList);
    (*ppList) = NULL;
}
