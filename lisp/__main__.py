#!/usr/bin/env python3

from .interpreter import run, evalquote, Atom, Pair

def _str2atom2(item):
    if isinstance(item, str):
        return Atom(item)
    elif isinstance(item, list):
        return str2atom(item)
    else:
        return item

def str2atom(lst):
    return [_str2atom2(item) for item in lst]

def list2pair(lst):
    if not isinstance(lst, list):
        return lst

    lst = str2atom(lst)

    if len(lst) == 2:
        return Pair(list2pair(lst[0]), list2pair(lst[1]))
    else:
        return Pair(list2pair(lst[0:-1]), list2pair(lst[-1]))

def DEFINE(name, x):
    return Pair(Atom(name), x)

def LAMBDA(args, body):
    return Pair(Atom("LAMBDA"), Pair(list2pair(args), body))
    #return Pair(Pair(Atom("LAMBDA"), list2pair(args)), body)

def COND(lst):
    return Pair(Atom("COND"), list2pair(lst))


def main():
    fn = Pair(Atom("HEAD"), Pair(Atom("TAIL"),
                                 Pair(Atom("1"), Pair(Atom("2"), Atom("3")))
        )))

    #fn = Atom("HEAD")
    #args = Pair(Atom("1"), Pair(Atom("2"), Atom("3")))
    print("fn   = " + str(fn))
    #print(run(fn))
    print(run(fn))
    exit()

    programs = [
        "(eq 1 1)",
        "(eq 1 2)",
        """
        (DEFINE MEMBER (LAMBDA (A X)
            (COND
                ((NULL X)           FALSE)
                ((EQ A (CAR X))     TRUE)
                (TRUE               (MEMBER A (SECOND X))))))

        (DEFINE UNION (LAMBDA (X Y)
            (COND
                ((NULL X)               Y)
                ((MEMBER (CAR X) Y)     (UNION (CDR X) Y))
                (TRUE                   (CONS (CAR X) (UNION (CDR X) Y))) )))

        (DEFINE INTERSECTION (LAMBDA (X Y)
            (COND
                ((NULL X)               NIL)
                ((MEMBER (CAR X) Y)     (CONS (CAR X) (INTERSECTION (CDR X) Y)))
                (TRUE                   (INTERSECTION (CDR X) Y)) )))

        (INTERSECTION ((A1 A2 A3) (A1 A3 A5)))
        (UNION ((X Y Z) (U V W X)))
        """
    ]

    programs = [
        (Atom("EQ"),
         Pair(Atom("1"), Atom("1")) ),

        (Atom("DEFINE"), Pair(Atom("MEMBER"),
            LAMBDA(['A', 'X'],
                  COND([
                    [["NULL", "X"],                 ["QUOTE", "FALSE"]],
                    [["EQ", "A", ["CAR", "X"]],     ["QUOTE", "TRUE"]],
                    [["QUOTE", "TRUE"],             ["MEMBER", "A", ["SECOND", "X"]]]]))
        )),

        (Atom("DEFINE"), Pair(Atom("UNION"),
            LAMBDA(['X', 'Y'],
                   COND([
                       [["NULL", "X"],                  "Y"],
                       [["MEMBER", ["CAR", "X"], "Y"],  ["UNION", ["CDR", "X"], "Y"]],
                       [["QUOTE", "TRUE"],             ["CONS", ["CAR", "X"], ["UNION", ["CDR", "X"], "Y"]]]
                    ])
            )
        )),

        (Atom("UNION"), list2pair([["X", "Y", "Z"], ["U", "V", "W", "X"]]))
    ]

    programs = [
        (Atom("NULL"), Atom("NIL")),

        (LAMBDA(['X', 'Y'],
                COND([
                    [["NULL", "X"],      "Y"],
                    [["NULL", "Y"],      "AAAAAAAAAAAA"],
                    [["QUOTE", "TRUE"],  "NIL"],
                ])),
         Pair('1', '2')),
    ]

    #programs = [
    #    (LAMBDA(['X'], ['X']), Atom('1'))
    #]

    for fn, args in programs:
        print("----")
        print("(" + str(fn) + "\n    " + str(args) + ")")
        print("=>")
        print(evalquote(fn, args))
        print()


main()
