%{

#include<stdio.h>
#include<string.h>
#include "bis.tab.h"
//extern yylval;
int fsd=0;

%}

keyword        "cin"|"cout"|"int"|"<<"|">>"
separator      ";"
operator       "-"|"+"|"*"|"/"|"="
id             [A-Z]
constant       0|-*[1-9]+[0-9]*

%%
{keyword} {
    yylval.id = strdup(yytext);
    return KEY;
}
{separator} {
    yylval.id = strdup(yytext);
    return SEP;
}
{operator} {
    yylval.id = strdup(yytext);
    return OP;
}
{constant} {
    yylval.id = strdup(yytext);
    return CONST;

}
{id} {
    yylval.id = strdup(yytext);
    return ID;
}
[ \t\n]+ { }
.        { }

%%

int yywrap() {}
