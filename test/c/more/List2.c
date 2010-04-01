/*
 *   List2.c
 *   3 Source File Example for SEng265
 *   Written by Glen Darling.
 */


#include <stdio.h>
#include <stdlib.h>


/* ALWAYS include your own header file */
#include "List2.h"


/* List functions */

extern void list_New( DigitList *pList ) {
    ( pList->List ) = NULL;
}

extern void list_Add( DigitList *pList, Digit digit ) {
    DigitListNodePtr out;
    out = (DigitListNodePtr) malloc( sizeof( DigitListNode ) );
    out->Data = digit;
    out->Next = pList->List;
    pList->List = out;
}

extern short list_Size( DigitList list ) {
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

extern Digit list_Nth( DigitList list, short n ) {
    DigitListNodePtr p;
    p = ( list.List );
    while( p != NULL ) {
        n--;
        if( !n )
            return( p->Data );
        p = ( p->Next );
    }
}

extern void list_Dispose( DigitList *pList ) {
    DigitListNodePtr p;
    p = ( pList->List );
    while( p != NULL ) {
        ( pList->List ) = p->Next;
        free( p );
        p = ( pList->List );
    }
    pList->List = NULL;
}
