names = {}


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
        evalInst(t[1])
        evalInst(t[2])
    elif t[0] == 'empty':
        return
    elif t[0] == 'print':
        print(evalExpr(t[1]))
    elif t[0] == 'printString':
        print(t[1])
    elif t[0] == 'assign':
        names[t[1]] = evalExpr(t[2])
    elif t[0] == 'if':
        if evalExpr(t[1]):
            evalInst(t[2])
    elif t[0] == 'for':
        evalInst(t[1])
        while evalExpr(t[2]):
            evalInst(t[4])
            evalInst(t[3])
    elif t[0] == 'while':
        while evalExpr(t[1]):
            evalInst(t[2])
