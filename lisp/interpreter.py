from dataclasses import dataclass

@dataclass(frozen=True)
class Atom:
    name: str

@dataclass(frozen=True)
class Pair:
    left: Atom
    right: Atom

GlobalVars = {}

NIL = Atom("NIL")

def first(x):
    if not isinstance(x, Pair):
        return NIL
    return x.left

def second(x: Pair):
    if not isinstance(x, Pair):
        return NIL

    return x.right


def fs(x):
    return first(second(x))

def fss(x):
    return first(second(second(x)))


def atom(x):
    return isinstance(x, Atom)

def eq(x, y):
    return x == y

def evcon(c, a):
    if l_eval(caar(c), a):
        return l_eval(cadar(c), a)
    else:
        return evcon(cdr(c), a)

def evlis(m: Pair, a):
    if m == Atom("NIL"):
        return NIL
    else:
        return cons(l_eval(first(m), a), evlis(second(m), a))

def l_eval(e, a):
    if atom(e):
        return second(assoc(e, a))
    elif atom(first(e)):
        if first(e) == Atom("QUOTE"):
            return cadr(e)
        elif first(e) == Atom("COND"):
            return evcon(second(e), a)
        else:
            return apply(first(e), evlis(second(e), a), a)
    else:
        return apply(first(e), evlis(second(e), a), a)


def apply(fn, x, a):
    if atom(fn):
        if fn == Atom("CAR"):
            return first(first(x))
        elif fn == Atom("CDR"):
            return second(first(x))
        elif fn == Atom("CONS"):
            return cons(first(x), fs(x))
        elif fn == Atom("ATOM"):
            return atom(first(x))
        elif fn == Atom("EQ"):
            return eq(first(x), fs(x))
        elif fn == Atom("DEFINE"):
            GlobalVars[x.left.name] = x.right
            return GlobalVars[x.left.name]
        else:
            return apply(l_eval(fn, a), x, a)
    elif first(fn) == Atom("LAMBDA"):
        return l_eval(fss(fn), pairlis(fs(fn), x, a))
    elif first(fn) == Atom("LABEL"):
        return apply(fss(fn), x, cons(cons(fs(fn), fss(fn), a)))

def evalquote(fn, x):
    return apply(fn, x, NIL)

