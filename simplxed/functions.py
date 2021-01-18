import numpy as np
from functools import reduce
from typing import List

'''
Check that inputs adhere to canonical form
'''
def is_canonical(c: List[float], A: List[List[float]], b: List[float]) -> bool:
    n = len(c)
    p = len(A)
    # Check all inputs are of non-zero length
    if (n == 0): return False
    if (p == 0): return False
    # Check that A is pxn matrix
    if (reduce(lambda acc,x: 1 if type(x) != list else 0, A) > 0): return False
    if (reduce(lambda acc,x: 1 if (len(x) != n) else 0, A) > 0): return False
    # Check that length of b matches num rows in A
    if (p != len(b)): return False
    # Check that all elements in b are non-negative
    if (reduce(lambda acc,x: 1 if (x < 0) else 0, b) > 0): return False
    return True

'''
Function to define an LP problem as a tableau
c is the 1xn vector of coefficients in the objective function
A is the pxn list where each inner list is a vector of coefficients 
for the respective constraint equation
b is the 1xp list of right-hand side values for the constraints
'''
def to_tableau(c: List[float], A: List[List[float]], b: List[float]) -> np.array([np.array([float])]):
    n = len(c)
    p = len(A)
    # Define the lower rows of tableau
    A_sub = np.array(A, dtype=float)
    slack_vars = np.eye(p, dtype=float)
    b_sub = np.reshape(np.array(b, dtype=float), (p,1))
    lower_rows = np.concatenate((np.zeros((p,1)),A_sub, slack_vars, b_sub), axis=1)
    # Define top row which corresponds to objective function
    c.insert(0, 1.0)
    t_sub = np.array(c, dtype=float)
    top_row = np.concatenate((t_sub, np.zeros((p+1))), axis=0)
    return np.insert(lower_rows, 0, top_row, axis=0)
