import pytest
from lisp.interpreter import *

def pair(a, b):
    if isinstance(a, str):
        a = Atom(a)
    if isinstance(b, str):
        b = Atom(b)
    return Pair(a, b)



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

@pytest.mark.skip()
def test_eval():
    ...

def test_run():
    # This also implicitly tests run().
    assert run(pair("HEAD", build_list(Atom("1"), Atom("2"), Atom("3")))) == Atom("1")
    assert run(pair("TAIL", build_list(Atom("1"), Atom("2"), Atom("3")))) == pair("2", "3")
    assert run(pair("HEAD", pair("TAIL", build_list("1", "2", "3")))) == Atom("2")
