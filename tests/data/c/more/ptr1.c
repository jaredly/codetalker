#include <stdio.h>

int main( int argc, char *argv[] ) {

        int a;

        a = 100;
        a++;
        a *= 5;

        printf( "&a = %p, a = %d (hex=%x,oct=%o)\n", &a, a, a, a );

        printf( "Ooops: %d\n", &a );
        printf( "Hex:   %x\n", &a );
        printf( "long:   %ld\n", &a );
        printf( "ptr:   %p\n", &a );
}


