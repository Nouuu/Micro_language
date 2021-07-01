import sys

import ply.lex as lex

from ply4ever.eval import evalInst
from ply4ever.genereTreeGraphviz import printTreeGraph

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'print': 'PRINT',
    'for': 'FOR',
    'while': 'WHILE',
    'function': 'FUNCTION',
    'return': 'RETURN'
}

tokens = [
             'NUMBER', 'MINUS', 'CHARS',
             'PLUS', 'TIMES', 'DIVIDE',
             'PLUSPLUS', 'PLUSEQUAL', 'MINUSMINUS', 'MINUSEQUAL',
             'LPAREN', 'RPAREN', 'LACO', 'RACO',
             'AND', 'OR', "EQUALS", "NAME", "SEMI", "COMA",
             "GREATER", "LOWER", "ISEQUAL"
         ] + list(reserved.values())

# Tokens
t_CHARS = r'".+"'
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
t_COMA = r','
t_ISEQUAL = r'=='
t_EQUALS = r'='
t_GREATER = r'>'
t_LOWER = r'<'


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
    p[0] = ('print', p[3], 'empty')


def p_statement_return(p):
    """statement : RETURN expression SEMI"""
    p[0] = ('return', p[2], 'empty')


def p_concatened_string(p):
    r"""STRING : CHARS
    | STRING PLUS expression
    | expression PLUS STRING"""
    if len(p) == 2:
        p[0] = ('string', p[1])
    else:
        p[0] = ('string', p[1], p[3])


def p_statement_print_string(p):
    r"""statement : PRINT LPAREN STRING RPAREN SEMI"""
    p[0] = ('print', p[3], 'empty')


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
    p[0] = ('if', p[2], p[5])


def p_parameters(p):
    """parameters : NAME
    | NAME COMA parameters"""
    if len(p) == 2:
        p[0] = ('param', 'empty', p[1])
    else:
        p[0] = ('param', p[3], p[1])


def p_expressions(p):
    """expressions : expression
    | expression COMA expressions"""
    if len(p) == 2:
        p[0] = ('param', 'empty', p[1])
    else:
        p[0] = ('param', p[3], p[1])


def p_function(p):
    """statement : FUNCTION NAME LPAREN parameters RPAREN LACO bloc RACO
    | FUNCTION NAME LPAREN RPAREN LACO bloc RACO"""
    if len(p) == 8:
        p[0] = ('function', p[2], p[6], 'empty')
    else:
        p[0] = ('function', p[2], p[7], p[4])


def p_void_expression(p):
    """statement : expression SEMI"""
    p[0] = ('bloc', p[1], 'empty')


def p_call_function(p):
    """expression : NAME LPAREN expressions RPAREN
    | NAME LPAREN RPAREN"""
    if len(p) == 4:
        p[0] = ('call', p[1], 'empty')
    else:
        p[0] = ('call', p[1], p[3])


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
    op = '+' if p[2] == '+=' else '-'
    p[0] = ('assign', p[1], (op, p[1], p[3]))


def p_expr_uminus(p):
    """expression : MINUS expression %prec UMINUS"""
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


# import ply.yacc as yacc
#
# yacc.yacc()


def load_files(yacc):
    if len(sys.argv) >= 2:
        for i in range(1, len(sys.argv)):
            with open(sys.argv[i], 'r') as file:
                yacc.parse(file.read())


def cli(yacc):
    while True:
        s = input('cmd (type exit(); to leave) > ')
        if s == "exit();":
            print("Bye bye !")
            return
        yacc.parse(s)

# # s = input('calc > ')
# s = '''
# fibo(10);
# printString("------------------");
# print(factorial(10));
# '''
# s2 = '''
# for (i=0; i < 10; i+=2;) { print(i); }
# '''
# yacc.parse(s)
