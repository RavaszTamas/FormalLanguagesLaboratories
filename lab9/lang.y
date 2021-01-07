%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #define YYDEBUG 1

%}

%token ID 1
%token CONST 2
%token osszead 3
%token kivon 4
%token szoroz 5
%token oszt 6
%token modulo 7
%token kisebb 8
%token kisebbvagyegyenlo 9
%token egyenlo 10
%token nagyobbvagyegyenlo 11
%token nagyobb 12
%token nemegyenlo 13
%token novel 14
%token csokken 15
%token kapja 16
%token ha 17
%token kulonben 18
%token karakter 19
%token karakterlanc 20
%token amig 21
%token boolean 22
%token egesz 23
%token tomb 24
%token dupla 25
%token visszater 26
%token ismeteld 27
%token Kezd 28
%token Vegez 29
%token allj 30
%token valassz 31
%token eset 32
%token alapertelmezett 33
%token konstans 34
%token open_square_bracket 35
%token closed_square_bracket 36
%token open_curly_bracket 37
%token closed_curly_bracket 38
%token open_bracket 39
%token closed_bracket 40
%token semicolon 41
%token coma 42
%token colon 43
%token olvas 44
%token kiir 45

%start program

%%
program : compoundstatement ;
compoundstatement : Kezd statementlist Vegez ;
statementlist : statement semicolon statementlist | statement ;
statement : declarationlist | simplestatement | structuredtatement ;
declarationlist : type identifierList ;
identifierList : ID coma identifierList | ID ;
type :  egesz | dupla | karakter | karakterlanc | boolean ;
simplestatement : assignment | iostatement ;
assignment : ID kapja expression ;
expression : term | term additive expression ;
term : factor| term multiplicative factor ;
factor : open_bracket expression closed_bracket | ID | CONST ;
additive : osszead | kivon ;
multiplicative : oszt | szoroz |  modulo ;
iostatement : olvas open_bracket value closed_bracket | kiir open_bracket value closed_bracket ;
value : ID | CONST ;
structuredtatement : ifstatement | whilestatement | forstatement ;
ifstatement : ha  open_bracket condition closed_bracket open_curly_bracket statement closed_curly_bracket | ha  open_bracket condition closed_bracket open_curly_bracket statement closed_curly_bracket kulonben open_curly_bracket statement closed_curly_bracket ;
condition : expression relation expression ;
whilestatement : amig open_bracket condition closed_bracket open_curly_bracket statementlist closed_curly_bracket ;
forstatement : ismeteld open_bracket statement semicolon statement semicolon statement closed_bracket open_curly_bracket statement closed_curly_bracket ;
relation : nemegyenlo | egyenlo | nagyobbvagyegyenlo | kisebbvagyegyenlo | kisebb | nagyobb ;
%%

int yyerror(char *s)
{
  printf("%s\n", s);
}

extern FILE *yyin;

int main(int argc, char **argv)
{
  if (argc > 1) 
    yyin = fopen(argv[1], "r");
  if ((argc>2) && (!strcmp(argv[2],"-d"))) 
    yydebug = 1;
  if (!yyparse()) 
    fprintf(stderr,"Successful parsing !!!\n");
}
