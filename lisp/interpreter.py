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

def equal(x, y):
    if atom(x):
        if atom(y):
            return eq(x, y)
        else:
            return False
    else:
        return False

def assoc(x, variables):
    print("  assoc(", x, ", ", variables, ")")
    if equal(first(first(variables)), x):
        return first(variables)
    else:
        return assoc(x, second(variables))

def pairlis(x, y, variables):
    if x == NIL:
        return variables
    else:
        return Pair(Pair(first(x), first(y)), pairlis(second(x), second(y), variables))

def evcon(c, variables):
    if l_eval(first(first(c)), variables):
        return l_eval(first(second(first(c))), variables)
    else:
        return evcon(second(c), variables)

def evlis(m: Pair, variables):
    if m == NIL:
        return NIL
    else:
        return Pair(l_eval(first(m), variables), evlis(second(m), variables))

def l_eval(e, variables):
    print("l_eval(", e, ", ", variables, ")")
    if atom(e):
        return second(assoc(e, variables))
    elif atom(first(e)):
        if first(e) == Atom("QUOTE"):
            return fs(e)
        elif first(e) == Atom("COND"):
            return evcon(second(e), variables)
        else:
            return apply(first(e), evlis(second(e), variables), variables)
    else:
        return apply(first(e), evlis(second(e), variables), variables)

def bool2atom(x):
    if x:
        return Atom("TRUE")
    else:
        return Atom("FALSE")

def apply(fn, args, variables):
    print("apply(", fn, ", ", args, ", ", variables, ")")
    if atom(fn):
        if fn == Atom("CAR"):
            return first(first(args))
        elif fn == Atom("CDR"):
            return second(first(args))
        elif fn == Atom("CONS"):
            return cons(first(args), fs(args))
        elif fn == Atom("ATOM"):
            return bool2atom(atom(first(args)))
        elif fn == Atom("EQ"):
            return bool2atom(eq(first(args), fs(args)))
        elif fn == Atom("DEFINE"):
            GlobalVars[args.left.name] = args.right
            return GlobalVars[args.left.name]
        elif fn.name in GlobalVars:
            return l_eval(fss(fn), pairlis(GlobalVars[fn.name], args, variables))
        #    return l_eval(GlobalVars[fn.name], variables)
        else:
            return apply(l_eval(fn, a), args, variables)
    elif first(fn) == Atom("LAMBDA"):
        return l_eval(fss(fn), pairlis(fs(fn), args, variables))
    elif first(fn) == Atom("LABEL"):
        return apply(fss(fn), args, Pair(Pair(fs(fn), fss(fn)), variables))
    else:
        exit("\n\n\n!!! No match in apply() for {}".format(fn))

def evalquote(fn, args):
    return apply(fn, args, NIL)
