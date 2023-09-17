#!/usr/bin/env python3

from .interpreter import evalquote, Atom, Pair

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
    lst = str2atom(lst)

    if len(lst) == 2:
        return Pair(lst[0], lst[1])
    else:
        return Pair(list2pair(lst[0:-1]), lst[-1])

def DEFINE(name, x):
    return Pair(Atom(name), x)

def LAMBDA(args, body):
    return Pair(list2pair(args), body)

def COND(lst):
    return Pair(Atom("COND"), list2pair(lst))


def main():
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
                    [["NULL", "X"],                 "FALSE"],
                    [["EQ", "A", ["CAR", "X"]],     "TRUE"],
                    ["TRUE",                        ["MEMBER", "A", ["SECOND", "X"]]]]))
        )),

        (Atom("DEFINE"), Pair(Atom("UNION"),
            LAMBDA(['X', 'Y'],
                   COND([
                       [["NULL", "X"],                  "Y"],
                       [["MEMBER", ["CAR", "X"], "Y"],  ["UNION", ["CDR", "X"], "Y"]],
                       [["TRUE",                        ["CONS", ["CAR", "X"], ["UNION", ["CDR", "X"], "Y"]]]]
                    ])
            )
        )),

        (Atom("UNION"), [["X", "Y", "Z"], ["U", "V", "W", "X"]])
    ]

    for fn, x in programs:
        print("----")
        print(fn)
        print(x)
        print("=>")
        print(evalquote(fn, x))
        print()

main()
