import pytest
from lisp.interpreter import *

def build_list(*args):
    if len(args) == 1:
        return args

    if len(args) == 2:
        return Pair(args[0], args[1])

    last, second_last, *rest = args[::-1]

    lst = Pair(second_last, last)
    for x in rest:
        lst = Pair(x, lst)
    return lst


def pair(a, b):
    if isinstance(a, str):
        a = Atom(a)
    if isinstance(b, str):
        b = Atom(b)
    return Pair(a, b)


def test_helper__pair():
    assert pair("a", "b") == Pair(Atom("a"), Atom("b"))
    assert pair("1", "2") == Pair(Atom("1"), Atom("2"))

def test_helper__build_list():
    de = Pair(Atom("D"), Atom("E"))
    cde = Pair(Atom("C"), de)
    bcde = Pair(Atom("B"), cde)
    expected = Pair(Atom("A"), bcde)
    assert build_list(Atom("A"), Atom("B"), Atom("C"), Atom("D"), Atom("E")) == expected


def test_first():
    assert first(Atom("1")) == Atom("1")
    assert first(Pair(Atom("1"), Atom("2"))) == Atom("1")

def test_second():
    assert second(Atom("1")) == NIL
    assert second(Pair(Atom("1"), Atom("2"))) == Atom("2")
    assert second(Pair(pair("1", "2"), pair("3", "4"))) == pair("3", "4")

@pytest.mark.skip()
def test_equal():
    ...

def test_assoc():
    b = pair("B",
             pair("CAR", "X"))
    c1 = pair("C",
              pair("QUOTE", "M"))
    c2 = pair("C",
              pair("CDR", "X"))
    variables = pair(b, pair(c1, c2))
    assert assoc(Atom("B"), variables) == b

def test_pairlis():
    au = pair("A", "U")
    bv = pair("B", "V")
    cw = pair("C", "W")
    dx = pair("D", "X")
    ey = pair("E", "Y")

    x = pair("A", pair("B", "C"))
    y = pair("U", pair("V", "W"))
    variables = pair(dx, ey)

    expected = pair(au, pair(bv, pair(cw, pair(dx, ey))))

    assert pairlis(x, y, variables) == expected

@pytest.mark.skip()
def test_evcon():
    ...

@pytest.mark.skip()
def test_evlist():
    ...

def test_eval():
    assert l_eval(Pair(Atom("1"), Atom("2")), Pair(Atom("NIL"), Atom("NIL"))) == Pair(Literal(1), Literal(2))

def test_run():
    # This also implicitly tests run().
    assert run(pair("HEAD", build_list(Atom("1"), Atom("2"), Atom("3")))) == Literal(1)
    assert run(pair("TAIL", build_list(Atom("1"), Atom("2"), Atom("3")))) == Pair(Literal(2), Literal(3))
    assert run(pair("HEAD", pair("TAIL", build_list(Atom("1"), Atom("2"), Atom("3"))))) == Atom("2")
