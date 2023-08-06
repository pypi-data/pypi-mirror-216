from gym_cas import *
import sympy.abc

def test_abc():
    assert a == sympy.abc.a
    assert x == sympy.abc.x

def fun(x):
    return x**2 + x

def test_abc_fun():
    assert fun(u)
    assert fun(1) == 2
    assert diff(fun(x),x)
    