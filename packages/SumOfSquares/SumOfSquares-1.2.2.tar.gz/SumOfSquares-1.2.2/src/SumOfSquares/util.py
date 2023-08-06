import sympy as sp
import numpy as np
import math
from operator import mul
from functools import reduce
from itertools import combinations

def prod(seq):
    return reduce(mul, seq, 1)

def factorial(n):
    return prod(range(1, n+1))

def binom(n, d):
    assert n >= d, f'invalid binom({n}, {d})!'
    return factorial(n)//factorial(n-d)//factorial(d)

def sum_tuple(t1, t2):
    return tuple(a1+a2 for a1, a2 in zip(t1, t2))

def is_hom(poly, deg):
    '''Determines if a polynomial POLY is homogeneous of degree DEG'''
    return sum(sum(m) != deg for m in poly.monoms()) == 0

def round_sympy_expr(expr, precision=3):
    '''Rounds all numbers in a sympy expression to stated precision'''
    return expr.xreplace({n : round(n, precision) for n in expr.atoms(sp.Number)})

def poly_degree(p, variables):
    '''Returns the max degree of P when treated as a polynomial in VARIABLES'''
    return sp.poly(p, variables).total_degree()

def orth(M):
    _, D, V = np.linalg.svd(M)
    return V[D >= 1e-9], V[D < 1e-9]

def get_poly_degree(vars, polys, deg=None):
    '''Given a vector of polynomials POLY, return minimum degree to run sum of
    squares, or check if DEG is above such minimum degree if provided'''
    max_deg = max(map(lambda p: poly_degree(p, vars), polys))
    if deg is None:
        deg = math.ceil(max_deg/2)
    if 2*deg < max_deg:
        raise ValueError(f'Degree of relaxation 2*{deg} less than maximum degree {max_deg}')
    return deg
