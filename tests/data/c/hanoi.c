/*

  HANOI.C
  =======
  (c) Paul Griffiths 1999
  Email: mail@paulgriffiths.net

  Outputs moves necessary to complete the
  "Towers of Hanoi" puzzle using a recursive function.

*/


#include <stdlib.h>
#include <string.h>
#include <stdio.h>


/*  Forward function declarations  */

void Hanoi       (int StartCol, int EndCol, int nDisks);
int  ParseCmdLine(int argc, char *argv[],
          int *StartCol, int *EndCol, int *nDisks);


/*  main() function  */

int main(int argc, char *argv[]) {
    int StartCol, EndCol, nDisks;


    /*  Set program variables  */
    
    if ( !ParseCmdLine(argc, argv, &StartCol, &EndCol, &nDisks) )
    exit(EXIT_FAILURE);


    /*  Output moves necessary  */

    printf("Towers of Hanoi!\n");
    printf("================\n\n");

    printf("To move %d disks from column %d to column %d...\n\n",
       nDisks, StartCol, EndCol);
    Hanoi(StartCol, EndCol, nDisks);

    exit(EXIT_SUCCESS);
}


/*  Output to stdin the moves necessary to move a stack
    of nDisks disks from column StartCol to column EndCol,
    according to the rules of the puzzle.                   */

void Hanoi(int StartCol, int EndCol, int nDisks) {
    if ( nDisks ) {
    Hanoi(StartCol, 6 - (StartCol + EndCol), nDisks - 1);
    printf("Move disk from column %d to column %d\n", StartCol, EndCol);
    Hanoi(6 - (StartCol + EndCol), EndCol, nDisks - 1);
    }
}


/*  Set program variables according to command line options  */

int ParseCmdLine(int argc, char *argv[],
         int *StartCol, int *EndCol, int *nDisks) {
    int n = 1;


    /*  Set default values for variables  */

    *nDisks   = 4;
    *StartCol = 1;
    *EndCol   = 2;


    /*  Set variables according to command line options  */

    while ( n < argc ) {
    if ( !strncmp(argv[n], "-d", 2) || !strncmp(argv[n], "-D", 2) ) {
        *nDisks = strtol(&argv[n][2], NULL, 0);
        if ( *nDisks < 1 ) {
        printf("Must have at least 1 disk to move!\n");
        return 0;
        }
    }
    else if ( !strncmp(argv[n], "-s", 2) || !strncmp(argv[n], "-S", 2) ) {
        *StartCol = strtol(&argv[n][2], NULL, 0);
        if ( *StartCol < 1 || *StartCol > 3 ) {
        printf("Start column must be 1, 2 or 3!\n");
        return 0;
        }
    }
    else if ( !strncmp(argv[n], "-e", 2) || !strncmp(argv[n], "-E", 2) ) {
        *EndCol = strtol(&argv[n][2], NULL, 0);
        if ( *EndCol < 1 || *EndCol > 3 ) {
        printf("End column must be 1, 2 or 3!\n");
        return 0;
        }
        if ( *EndCol == *StartCol ) {
        printf("Start column and end column must be different!\n");
        return 0;
        }
    }
    ++n;
    }
    return 1;
}

