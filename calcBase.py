import ply.lex as lex

from eval import evalInst
from genereTreeGraphviz import printTreeGraph

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'print': 'PRINT',
    'printString': 'PRINTSTRING',
    'for': 'FOR',
    'while': 'WHILE',
}

tokens = [
             'NUMBER', 'MINUS', 'STRING',
             'PLUS', 'TIMES', 'DIVIDE',
             'PLUSPLUS', 'PLUSEQUAL', 'MINUSMINUS', 'MINUSEQUAL',
             'LPAREN', 'RPAREN', 'LACO', 'RACO',
             'AND', 'OR', "EQUALS", "NAME", "SEMI",
             "GREATER", "LOWER", "ISEQUAL"
         ] + list(reserved.values())

# Tokens
t_STRING = r'".+"'
t_PLUSPLUS = r'\+\+'
t_PLUSEQUAL = r'\+='
t_MINUSMINUS = r'\-\-'
t_MINUSEQUAL = r'\-='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LACO = r'\{'
t_RACO = r'\}'
t_AND = r'&'
t_OR = r'\|'
t_SEMI = r';'
t_EQUALS = r'='
t_GREATER = r'>'
t_LOWER = r'<'
t_ISEQUAL = r'=='


def t_NAME(t):
    r"""[a-zA-Z_][a-zA-Z0-9_]*"""
    t.type = reserved.get(t.value, "NAME")
    return t


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t\n\r"

def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer

lex.lex()

precedence = (
    ('nonassoc', 'ISEQUAL', 'LOWER', 'GREATER'),
    ('nonassoc', 'AND', 'OR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'PLUSPLUS', 'PLUSEQUAL', 'MINUSMINUS', 'MINUSEQUAL'),
    ('right', 'UMINUS'),
)


def p_start(p):
    """start : bloc"""
    p[0] = p[1]
    print(p[0])
    printTreeGraph(p[0])
    evalInst(p[1])


def p_bloc(p):
    """bloc : bloc statement
    | statement"""
    if len(p) == 3:
        p[0] = ('bloc', p[1], p[2])
    else:
        p[0] = ('bloc', p[1], 'empty')


def p_statement_assign(p):
    """statement : NAME EQUALS expression SEMI"""
    # names[p[1]] = p[3]
    p[0] = ('assign', p[1], p[3])


def p_statement_print(p):
    """statement : PRINT LPAREN expression RPAREN SEMI"""
    p[0] = ('print', p[3])


def p_statement_print_string(p):
    r"""statement : PRINTSTRING LPAREN STRING RPAREN SEMI"""
    p[0] = ('printString', p[3].strip("\""))


def p_expression_binop(p):
    """expression : expression PLUS expression
                | expression TIMES expression
                | expression MINUS expression
                | expression DIVIDE expression
                | expression AND expression
                | expression OR expression
                | expression GREATER expression
                | expression LOWER expression
                | expression ISEQUAL expression"""
    p[0] = (p[2], p[1], p[3])


def p_condition(p):
    """statement : IF expression THEN LACO bloc RACO"""
    p[0] = ('if', p[2], p[4])


def p_loop_for(p):
    """statement : FOR LPAREN statement expression SEMI statement RPAREN LACO bloc RACO"""
    p[0] = ('for', p[3], p[4], p[6], p[9])


def p_loop_while(p):
    """statement : WHILE expression LACO bloc RACO"""
    p[0] = ('while', p[2], p[4])


def p_expression_inc(p):
    """statement : NAME PLUSPLUS SEMI
    | NAME MINUSMINUS SEMI"""
    op = '+' if p[2] == '++' else '-'
    p[0] = ('assign', p[1], (op, p[1], 1))


def p_expression_inc_n(p):
    """statement : NAME PLUSEQUAL expression SEMI
    | NAME MINUSEQUAL expression SEMI"""
    op = '+' if p[2] == '++' else '-'
    p[0] = ('assign', p[1], (op, p[1], p[3]))


def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_expression_name(p):
    """expression : NAME"""
    # p[0] = names[p[1]]
    p[0] = p[1]


def p_error(p):
    print("Syntax error at '%s'" % p.value)


import ply.yacc as yacc

yacc.yacc()

# s = input('calc > ')
s = '''
first=0;
second=1;
i=10;
while i> 0 {
    tmp=first+second;
    first=second;
    second=tmp;
    print(first);
    i-=2;
    i++;
}
printString("This is a string");
'''
yacc.parse(s)
