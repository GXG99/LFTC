bison -d bis.y
flex lex.l

gcc bis.tab.c lex.yy.c -o output.exe
