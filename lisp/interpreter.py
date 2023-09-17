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
    match [x, y]:
        case [Atom(_), Atom(_)]:
            return eq(x, y)
        case [Pair(_, _), Pair(_, )]:
            return equal(first(x), first(y)) and equal(second(x), second(y))
        case _:
            return False

def assoc(x, variables):
    print("\nassoc/variables=", variables, " [x=", x, "]")
    #print("  assoc(", x, ", ", variables, ")")
    if equal(first(first(variables)), x):
        return first(variables)
    else:
        return assoc(x, second(variables))

def pairlis(x, y, variables):
    print("pairlis")
    print("  x   =", x)
    print("  y   =", y)
    print("  vars=", variables)
    if x == NIL:
        return variables
    else:
        return Pair(Pair(first(x), first(y)), pairlis(second(x), second(y), variables))

def evcon(c, variables):
    print("evcon")
    print("  c   =", c)
    print("  vars=", variables)

    print(first(first(c)), "=>")
    print(l_eval(first(first(c)), variables))

    exit()
    if l_eval(first(first(c)), variables):
        return l_eval(first(second(first(c))), variables)
    else:
        return evcon(second(c), variables)

def evlis(m: Pair, variables):
    print("\nevlis")
    print("     m=", m)
    print("  vars=", variables)
    if m == NIL:
        return NIL
    else:
        print("  ?")
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
    print("\nl_eval")
    print("  form=", form)
    print("  variables=", variables)
    #print("l_eval/variables=", variables)
    if form == Atom("COND"):
        raise

    match form:
        case Atom("NIL"):
            return Atom("NIL")
        case Atom(name):
            if is_int(name):
                return int(name)

            if is_float(name):
                return float(name)

            # I think this is where function lookups go?
            if name in GlobalVars:
                return GlobalVars[name]
            else:
                print("!! form.name=", name)
                print("!! GlobalVars.keys()=", GlobalVars.keys())
                return second(assoc(form, variables))
        case [Atom("QUOTE"), _]:
            return second(form)
        #case [Atom("FUNCTION"), _]:
        #    # TODO: Figure out what FUNCTION does.
        case [Atom("COND"), _]:
            return evcon(second(form), variables)
        #case [Atom("PROG"), _]:
        #    # TODO: Figure out what PROG does.
        case Pair(Atom(a), b):
            # From page 71 of _LISP 1.5 Programmers Manual_.
            return l_eval(Pair(second(assoc(first(form), variables))), second(form), variables)
        case _:
            print("  case _:")
            print("    first(form) =", first(form))
            print("    second(form)=", second(form))
            print("    variables   =", variables)
            return apply(first(form), evlis(second(form), variables), variables)

def bool2atom(x):
    if x:
        return Atom("TRUE")
    else:
        return Atom("FALSE")


def apply(fn, args, variables):
    print("apply")
    print("  fn  =", fn)
    print("  args=", args)
    print("  vars=", variables)
    match fn:
        case Atom("NIL"):
            return NIL
        case Atom("CAR"):
            return first(first(args))
        case Atom("CDR"):
            return second(first(args))
        case Atom("CONS"):
            return cons(first(args), fs(args))
        case Atom("ATOM"):
            return bool2atom(atom(first(args)))
        case Atom("EQ"):
            return bool2atom(eq(first(args), fs(args)))
        case Atom("NULL"):
            return first(args) == NIL
        case Atom("DEFINE"):
            GlobalVars[args.left.name] = args.right
            return GlobalVars[args.left.name]
        case Pair(Atom("LAMBDA"), Pair(arg_names, fn_body)):
            print()
            print()
            print("apply/LAMBDA")
            print("    fn=", fn)
            print("    arg_names=", arg_names)
            print("    args=", args)
            print("    fn_body=", fn_body)
            print()
            print()
            #return l_eval(fss(fn), nconc(Pair(cadr(fn), args), variables))

            # This line causes (LAMBDA (X Y) (COND ...)) called with (1 2) to
            # wind up running l_eval with:
            #   form=COND
            #   vars=((X . 1) . ((NIL . NIL) . NIL))
            return l_eval(fn_body, pairlis(arg_names, args, variables))
        case Pair(Atom("LABEL"), _):
            return apply(fss(fn), args, Pair(Pair(fs(fn), fss(fn)), variables))
        case _:
            return apply(l_eval(fn, variables), args, variables)

def evalquote(fn, args):
    return apply(fn, args, NIL)
