%{
        /* Definition section */
    #include <stdio.h>
    #include<stdlib.h>
    #include <string.h>
    #define YYDEBUG 1
    extern FILE* yyin;
    extern FILE* yyout;
    int eflag=0;
    int yylex();

    int codeCounter = 0;
    int dataCounter = 0;

    char codeSegment[10000];
    char dataSegment[10000];

    /* For printing error messages */
    int yyerror(char* s) {
        printf("\nsyntax error\n");
        eflag=1;
    }

    void writeToFile();

%}
 
%union {
    char* id;
}

%token <id> ID SEP OP KEY CONST
%%
prog: statements ;
statements: | statement statements ;

statement:  KEY ID SEP {
    if (strcmp($1, "int") == 0) {
        char *temp;
        sprintf(temp, "\t%s dw 0\n", $2);
        strcat(dataSegment, temp);
    }
}          
|KEY KEY ID SEP{
    if (strcmp($1, "cout") == 0 && strcmp($2, "<<") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Printing variable\n\t\tmov eax, [%s]\n\t\tpush dword eax\n\t\tpush dword format\n\t\tcall [printf]\n\t\tadd esp, 4 * 2\n", $3);
        strcat(codeSegment, temp);
        free(temp);
    }
    if (strcmp($1, "cin") == 0 && strcmp($2, ">>") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Reading variable\n\t\tpush dword %s\n\t\tpush dword format\n\t\tcall [scanf]\n\t\tadd esp, 4 * 2\n", $3);
        strcat(codeSegment, temp);
        free(temp);
    }
}

|ID OP CONST SEP {
    if (strcmp($2, "=") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Assignment\n\t\tmov dword [%s], %s\n", $1, $3);
        strcat(codeSegment, temp);
        free(temp);
    }
}

|ID OP CONST OP CONST SEP {
    if (strcmp($4, "+") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Adding\n\t\tmov AX, %s\n\t\tmov BX, %s\n\t\tadd AX, BX\n\t\tmov [%s], AX\n", $3, $5, $1);
        strcat(codeSegment, temp);
        free(temp);
    }
    if (strcmp($4, "-") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Substracting\n\t\tmov AX, %s\n\t\tmov BX, %s\n\t\tsub AX, BX\n\t\tmov [%s], AX\n", $3, $5, $1);
        strcat(codeSegment, temp);
        free(temp);
    }
    if (strcmp($4, "*") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Multiply\n\t\tmov AX, %s\n\t\tmov BX, %s\n\t\tmul BX\n\t\tpush DX\n\t\tpush AX\n\t\tpop EAX\n\t\tmov [%s], EAX\n", $3, $5, $1);
        strcat(codeSegment, temp);
        free(temp);
    }
    if (strcmp($4, "/") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Division\n\t\tmov AX, %s\n\t\tmov DX, 0\n\t\tmov BX, %s\n\t\tdiv word BX\n\t\tmov [%s], AX\n", $3, $5, $1);
        strcat(codeSegment, temp);
        free(temp);
    }
}

| ID OP ID OP CONST SEP {
    if (strcmp($4, "+") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Adding\n\t\tmov AX, [%s]\n\t\tmov BX, %s\n\t\tadd AX, BX\n\t\tmov [%s], AX\n", $3, $5, $1);
        strcat(codeSegment, temp);
        free(temp);
    }
    if (strcmp($4, "-") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Substracting\n\t\tmov AX, %s\n\t\tmov BX, %s\n\t\tsub AX, BX\n\t\tmov [%s], AX\n", $3, $5, $1);
        strcat(codeSegment, temp);
        free(temp);
    }
}
| ID OP ID OP ID SEP {
    if (strcmp($4, "+") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Adding\n\t\tmov AX, [%s]\n\t\tmov BX, [%s]\n\t\tadd AX, BX\n\t\tmov [%s], AX\n", $3, $5, $1);
        strcat(codeSegment, temp);
        free(temp);
    }
    if (strcmp($4, "-") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Substracting\n\t\tmov AX, [%s]\n\t\tmov BX, [%s]\n\t\tsub AX, BX\n\t\tmov [%s], AX\n", $3, $5, $1);
        strcat(codeSegment, temp);
        free(temp);
    }
}

| ID OP CONST OP ID SEP {
    if (strcmp($4, "+") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Adding\n\t\tmov AX, %s\n\t\tmov BX, %s\n\t\tadd AX, BX\n\t\tmov [%s], AX\n", $3, $5, $1);
        strcat(codeSegment, temp);
        free(temp);
    }
    if (strcmp($4, "-") == 0) {
        char *temp = (char *)malloc(sizeof(char) * 300);
        sprintf(temp, "\t;Substracting\n\t\tmov AX, %s\n\t\tmov BX, %s\n\t\tsub AX, BX\n\t\tmov [%s], AX\n", $3, $5, $1);
        strcat(codeSegment, temp);
        free(temp);
    }
};

%%
 
int main(int argc,char** argv) {

    if (argc > 1)
    {
        FILE *file1;
        file1 = fopen(argv[1], "r");
        if (!file1)
        {
            fprintf(stderr, "Could not open %s\n", argv[1]);
            exit(1);
        }
        
        yyin = file1;
    }

    yydebug=1;
    yyparse();
    if(eflag==0) {
        printf("\n---success---\n");
    }
    writeToFile();
}
 
void writeToFile() {
        FILE *file2 = fopen("program.asm", "w");
        fprintf(file2, "bits 32\nglobal start\nextern exit, printf, scanf\nimport exit msvcrt.dll\nimport printf msvcrt.dll\nimport scanf msvcrt.dll\n\n");
        fprintf(file2, "segment data use32 class=data\n\tformat db \"%%d\", 10, 0\n");
        fprintf(file2, dataSegment);
        fprintf(file2, "\nsegment  code use32 class=code\n\tstart:\n");
        fprintf(file2, codeSegment);
        fprintf(file2, "\n\t\tpush dword 0\n\t\tcall [exit]");
}