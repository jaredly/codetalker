
default:
	rm -f codetalker/pgm/cgrammar/*.c codetalker/pgm/cgrammar/*.so
	pyx codetalker/pgm/cgrammar/process
	pyx codetalker/pgm/cgrammar/parser
	pyx codetalker/pgm/cgrammar/tokenize
	pyx codetalker/pgm/cgrammar/convert
