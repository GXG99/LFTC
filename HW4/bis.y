%{
    /* Definition section */
  #include <stdio.h>
  int eflag=0;

%}
 
%token CONST ID SEP OP KEY REL 

%%
prog: statements ;
statements: | statement statements ;

operand: ID|CONST ;
loop: KEY SEP operand REL operand SEP SEP statements SEP ;

statement: KEY ID SEP
            |KEY SEP ID SEP
            |KEY SEP CONST
            |ID OP CONST
            |ID OP ID
            |loop {printf("statement");};
%%
 
int main() {
    printf("start\n");
    yyparse();
    if(eflag==0){
        printf("\nsuccess\n");
    }
}
 
/* For printing error messages */
int yyerror(char* s) {
    printf("\ninvalid input\n");
    eflag=1;
}