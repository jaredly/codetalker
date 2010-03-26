YFLAGS	= -dv
CFLAGS	= -O
LFLAGS	=

SRC	= gram.y scan.l main.c
OBJ	= gram.o scan.o main.o

all:	$(OBJ)
	cc $(CFLAGS) $(OBJ) -o cparser

scan.o:	y.tab.h

scan.c: scan.l
	lex -t scan.l > scan.c

gram.o:	gram.c

gram.c:	gram.y
	yacc -dv gram.y
	mv -f y.tab.c gram.c
	
	
clean:; rm -f cparser y.output gram.c scan.c *.o
