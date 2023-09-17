from dataclasses import dataclass

@dataclass(frozen=True)
class Atom:
    name: str

    def __str__(self):
        return self.name

@dataclass(frozen=True)
class Pair:
    left: Atom
    right: Atom

    def __str__(self):
        return "({} . {})".format(self.left, self.right)

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
    print("assoc/variables=", variables, " [x=", x, "]")
    #print("  assoc(", x, ", ", variables, ")")
    if equal(first(first(variables)), x):
        return first(variables)
    else:
        return assoc(x, second(variables))

def pairlis(x, y, variables):
    print("pairlis/variables=", variables)
    if x == NIL:
        return variables
    else:
        return Pair(Pair(first(x), first(y)), pairlis(second(x), second(y), variables))

def evcon(c, variables):
    print("evcon/variables=", variables)
    if l_eval(first(first(c)), variables):
        return l_eval(first(second(first(c))), variables)
    else:
        return evcon(second(c), variables)

def evlis(m: Pair, variables):
    print("evlis/variables=", variables)
    if m == NIL:
        return NIL
    else:
        return Pair(l_eval(first(m), variables), evlis(second(m), variables))

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    # If `is_int(s)` returns True, it's an integer -- although `float(s)`
    # will happily take it anyway.
    if is_int(s):
        return False

    try:
        float(s)
        return True
    except ValueError:
        return False

def l_eval(form, variables):
    print("l_eval")
    print("  form=", form)
    print("  variables=", variables)
    #print("l_eval/variables=", variables)
    if form == Atom("COND"):
        raise

    if form == NIL:
        return NIL
    elif atom(form):
        if is_int(form.name):
            return int(form.name)

        if is_float(form.name):
            return float(form.name)

        # I think this is where function lookups go?
        if form.name in GlobalVars:
            return GlobalVars[form.name]
        else:
            print("!! form.name=", form.name)
            print("!! GlobalVars.keys()=", GlobalVars.keys())
            return second(assoc(form, variables))
    elif first(form) == Atom("QUOTE"):
        return second(form)
    #elif first(form).name == "FUNCTION":
    #    # TODO: Figure out what FUNCTION does.
    elif first(form) == Atom("COND"):
        return evcon(second(form), variables)
    #elif first(form).name == "PROG":
    #    # TODO: Figure out what PROG does.
    elif atom(first(form)):
        #if first(form) == Atom("QUOTE"):
        #    return fs(form)
        #elif first(form) == Atom("COND"):
        #    return evcon(second(form), variables)
        #else:
        #    return apply(first(form), evlis(second(form), variables), variables)

        # TODO: See page 71 of _LISP 1.5 Progammers Manual_.
        #if ...:
        #    ...
        #else:
        # should it be assoc(first(form), variables, NIL? Not sure what the symbol the paper used means...)
        return l_eval(Pair(second(assoc(first(form), variables, NIL))), second(form), variables)
    else:
        return apply(first(form), evlis(second(form), variables), variables)

def bool2atom(x):
    if x:
        return Atom("TRUE")
    else:
        return Atom("FALSE")


GLOBALS = []
def apply(fn, args, variables):
    #if variables == NIL:
    #    variables = GLOBALS
    #print("apply(fn=" + str(fn) + ", ..., ...)")
    if fn == NIL:
        return NIL
    elif atom(fn):
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
        elif fn == Atom("NULL"):
            return first(args) == NIL
        elif fn == Atom("DEFINE"):
            #print("DEFINE:")
            #print("  fn=", fn)
            #print("  args.right=", args.right)
            #print("  args.right.right=", args.right.right)
            #GLOBALS.append(Pair(args.left, args.right))
            #return Atom("TRUE")
            GlobalVars[args.left.name] = args.right
            return GlobalVars[args.left.name]
        #elif fn.name in GlobalVars:
        #    return l_eval(fss(fn), pairlis(GlobalVars[fn.name], args, variables))
        #    return l_eval(GlobalVars[fn.name], variables)
        else:
            return apply(l_eval(fn, variables), args, variables)
    elif first(fn) == Atom("LAMBDA"):
        print()
        print()
        print("apply/LAMBDA")
        print("    fn=", fn)
        print()
        print("  args is" + (" " if isinstance(args, Pair) else " NOT") + "a Pair()")
        print()
        print()
        #return l_eval(fss(fn), nconc(Pair(cadr(fn), args), variables))

        # This line causes (LAMBDA (X Y) (COND ...)) called with (1 2) to
        # wind up running l_eval with:
        #   form=COND
        #   vars=((X . 1) . ((NIL . NIL) . NIL))
        return l_eval(fss(fn), pairlis(fs(fn), args, variables))
    elif first(fn) == Atom("LABEL"):
        return apply(fss(fn), args, Pair(Pair(fs(fn), fss(fn)), variables))
    else:
        apply(l_eval(fn, variables), arguments, variables)

def evalquote(fn, args):
    return apply(fn, args, NIL)
