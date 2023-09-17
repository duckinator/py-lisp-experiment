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
    print("eq(", x, ", ", y, ")")
    return x == y

def equal(x, y):
    if atom(x):
        if atom(y):
            return eq(x, y)
        else:
            return False
    else:
        return False

def assoc(x, a):
    print("  assoc(", x, ", ", a, ")")
    if equal(first(first(a)), x):
        return first(a)
    else:
        return assoc(x, second(a))

def evcon(c, a):
    if l_eval(first(first(c)), a):
        return l_eval(first(second(first(c))), a)
    else:
        return evcon(second(c), a)

def evlis(m: Pair, a):
    if m == Atom("NIL"):
        return NIL
    else:
        return Pair(l_eval(first(m), a), evlis(second(m), a))

def l_eval(e, a):
    print("l_eval(", e, ", ", a, ")")
    if atom(e):
        return second(assoc(e, a))
    elif atom(first(e)):
        if first(e) == Atom("QUOTE"):
            return fs(e)
        elif first(e) == Atom("COND"):
            return evcon(second(e), a)
        else:
            return apply(first(e), evlis(second(e), a), a)
    else:
        return apply(first(e), evlis(second(e), a), a)

def bool2atom(x):
    if x:
        return Atom("TRUE")
    else:
        return Atom("FALSE")

def apply(fn, x, a):
    print("apply(", fn, ", ", x, ", ", a, ")")
    if atom(fn):
        if fn == Atom("CAR"):
            return first(first(x))
        elif fn == Atom("CDR"):
            return second(first(x))
        elif fn == Atom("CONS"):
            return cons(first(x), fs(x))
        elif fn == Atom("ATOM"):
            return bool2atom(atom(first(x)))
        elif fn == Atom("EQ"):
            return bool2atom(eq(first(x), fs(x)))
        elif fn == Atom("DEFINE"):
            GlobalVars[x.left.name] = x.right
            return GlobalVars[x.left.name]
        elif fn.name in GlobalVars:
            return GlobalVars
        else:
            return apply(l_eval(fn, a), x, a)
    elif first(fn) == Atom("LAMBDA"):
        return l_eval(fss(fn), pairlis(fs(fn), x, a))
    elif first(fn) == Atom("LABEL"):
        return apply(fss(fn), x, Pair(Pair(fs(fn), fss(fn)), a))

def evalquote(fn, x):
    return apply(fn, x, NIL)
