names = {}
functions = {}

def evalExpr(t):
    if type(t) is not tuple:
        if type(t) is int or type(t) is float:
            return t
        if t.lower() == 'true' or t.lower() == 'vrai':
            return True
        if t.lower() == 'false' or t.lower() == 'faux':
            return False
        return names[t]
    if t[0] == '+':
        return evalExpr(t[1]) + evalExpr(t[2])
    if t[0] == '*':
        return evalExpr(t[1]) * evalExpr(t[2])
    if t[0] == '-':
        return evalExpr(t[1]) - evalExpr(t[2])
    if t[0] == '/':
        return evalExpr(t[1]) / evalExpr(t[2])
    if t[0] == '&':
        return evalExpr(t[1]) and evalExpr(t[2])
    if t[0] == '|':
        return evalExpr(t[1]) or evalExpr(t[2])
    if t[0] == '>':
        return evalExpr(t[1]) > evalExpr(t[2])
    if t[0] == '<':
        return evalExpr(t[1]) < evalExpr(t[2])
    if t[0] == '==':
        return evalExpr(t[1]) == evalExpr(t[2])
    raise ValueError("Can't parse this ", t)


def evalInst(t):
    if t[0] == 'bloc':
        eval_bloc(t)
    elif t[0] == 'empty':
        return
    elif t[0] == 'print':
        print(evalExpr(t[1]))
    elif t[0] == 'printString':
        print(t[1])
    elif t[0] == 'assign':
        eval_assign(t)
    elif t[0] == 'if':
        eval_if(t)
    elif t[0] == 'for':
        eval_for(t)
    elif t[0] == 'while':
        eval_while(t)


def eval_bloc(t):
    evalInst(t[1])
    evalInst(t[2])


def eval_while(t):
    while evalExpr(t[1]):
        evalInst(t[2])


def eval_assign(t):
    names[t[1]] = evalExpr(t[2])


def eval_for(t):
    evalInst(t[1])
    while evalExpr(t[2]):
        evalInst(t[4])
        evalInst(t[3])


def eval_if(t):
    if evalExpr(t[1]):
        evalInst(t[2])
