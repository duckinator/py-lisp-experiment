from lisp.interpreter import *

def test_first():
    assert first(Atom("1")) == Atom("1")
    assert first(Pair(Atom("1"), Atom("2"))) == Atom("1")

def test_second():
    assert second(Atom("1")) == NIL
    assert second(Pair(Atom("1"), Atom("2"))) == Atom("2")

def test_equal():
    ...

def test_assoc():
    ...

def test_pairlis():
    ...

def test_evcon():
    ...

def test_evlist():
    ...

def test_eval():
    ...

def test_apply():
    ...
