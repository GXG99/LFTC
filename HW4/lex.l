%{

#include<stdio.h>
#include<string.h>
#include "bis.tab.h"
extern int yylval;

int atoms=0;
int fipAtoms=0;
int i;
char ts[50][9];
char fip[100][10];
char c[10];
char ind[2];

int flag=0;

%}

keyword        "if"|"else"|"while"|"cin"|"cout"|"int"|"<<"|">>"
separator      "("|")"|";"|"{"|"}"
relation       ">"|"<"|"!="|"=="|"="
operator       "-"|"+"|"*"|"/"|"%"
id             [a-z]{1,250}
constant       [1-9]+[0-9]*

%%
{keyword} {
    strcpy(c,yytext);
    strcat(c," -1");
    strcpy(fip[fipAtoms],c);
    fipAtoms+=1;

}
{separator} {

    strcpy(c,yytext);
    strcat(c," -1");
    strcpy(fip[fipAtoms],c);
    fipAtoms+=1;

}
{relation} {

    strcpy(c,yytext);
    strcat(c," -1");
    strcpy(fip[fipAtoms],c);
    fipAtoms+=1;



}
{operator} {

    strcpy(c,yytext);
    strcat(c," -1");
    strcpy(fip[fipAtoms],c);
    fipAtoms+=1;

}
{constant} {

    
    for(i=0;i<atoms;i++){
        if(strcmp(ts[i],yytext)==0){
            flag=1;
        }
    }
    if(flag==0){
        strcpy(ts[atoms],yytext);
        strcpy(c,yytext);
        sprintf(ind," %d",atoms);
        strcat(c,ind);
        strcpy(fip[fipAtoms],c);
        atoms+=1;
        fipAtoms+=1;
    } else flag=0;


}
{id} {

    for(i=0;i<atoms;i++){
        if(strcmp(ts[i],yytext)==0){
            flag=1;
        }
    }
    if(flag==0){
        strcpy(ts[atoms],yytext);
        strcpy(c,yytext);
        sprintf(ind," %d",atoms);
        strcat(c,ind);
        strcpy(fip[fipAtoms],c);
        atoms+=1;
        fipAtoms+=1;
    } else flag=0;

}
[ \t\n]+ { }
.        { printf("error at %s \n",yytext); }

%%

int yywrap() {}

int main(int argc,char** argv){
    if (argc > 1)
    {
        FILE *file;
        file = fopen(argv[1], "r");
        if (!file)
        {
            fprintf(stderr, "Could not open %s\n", argv[1]);
            exit(1);
        }
        yyin = file;
    }
    

    yylex();

    FILE *f = fopen("fip.txt","a"); 
    for(i=0;i<atoms;i++){
        printf("%s %d\n",ts[i],i);
    }
    for(i=0;i<fipAtoms;i++){
        fprintf(f,"%s\n",fip[i]);
    }
    printf("end");

    return 0;
}