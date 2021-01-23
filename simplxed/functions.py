import numpy as np
import copy
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
    for x in A:
        if (type(x) != list): return False
        if (len(x) != n): return False
    # Check that length of b matches num rows in A
    if (p != len(b)): return False
    # Check that all elements in b are non-negative
    for y in b:
        if (y < 0): return False
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
    c_cop = copy.copy(c)
    c_cop.insert(0, 1.0)
    t_sub = np.array(c_cop, dtype=float)
    top_row = np.concatenate((t_sub, np.zeros((p+1))), axis=0)
    return np.insert(lower_rows, 0, top_row, axis=0)

class LP:
    def __init__(self, c: List[float], A: List[List[float]], b: List[float]):
        if (not is_canonical(c,A,b)):
            raise ValueError("Inputs do not adhere to canonical form")
        else:
            self.tab = to_tableau(c,A,b)
            self.pcol = None
            self.prow = None

    # Decode the current tableau into feasible solution
    # Soultion returned is array of form :
    # [ x_1, ... ,x_n, s_1, ... ,s_n, optimal_function_value ]
    def decode(self):
        n = self.tab.shape[1]-2
        solution = [None]*n
        for i in range(1,self.tab.shape[1]-1):
            col = self.tab[:,i]
            # Check if col is a basic var
            if (np.count_nonzero(col==0) == self.tab.shape[0]-1):
                # Calculate value accordingly
                idx = np.nonzero(col)
                value = self.tab[idx,-1]/col[idx]
                solution[i-1] = value[0][0]
            else:
                solution[i-1] = 0
        solution.append(self.tab[0,-1])
        return solution

    # Choose the pivot column w.r.t. current tableau state
    def getPivCol(self):
        # Bland's rule used since argmin returns first occurrence
        entv = np.argmin(self.tab[0][1:-1])+1
        self.pcol = entv

    # Conduct ratio test to choose pivot row
    def getPivRow(self):
        if (not self.pcol):
            raise ValueError("pcol attribute must be set to obtain prow")
        tgt_col = self.tab[:,self.pcol]
        rhs_col = self.tab[:,-1]
        non_zero_idx = np.nonzero(tgt_col>0)[0]
        non_zero_vals = tgt_col[non_zero_idx]
        rhs_vals = rhs_col[non_zero_idx]
        ratios = np.divide(rhs_vals, non_zero_vals)
        self.prow = non_zero_idx[np.argmin(ratios)]

    # Execute a tableau pivot
    def pivot(self):
        if (not self.prow):
            raise ValueError("prow and pcol attribute must be set to execute pivot")
        piv_val = self.tab[self.prow, self.pcol]
        multipliers = np.divide(self.tab[:,self.pcol]*-1., piv_val)
        multipliers[self.prow] = 1.0/piv_val
        init_transf = [self.tab[self.prow,:]*mult for mult in multipliers]
        pivoted_tab = np.add(init_transf, self.tab)
        pivoted_tab[self.prow] = init_transf[self.prow]
        self.tab = pivoted_tab

    # Iteratively pivot until optimal solution found
    def optimize(self, max_iter: int = 10000):
        counter = 1
        while ((np.count_nonzero(self.tab[0]<0) > 0) or (counter < max_iter)):
            self.getPivCol()
            self.getPivRow()
            self.pivot()
            counter += 1
        if (counter < max_iter):
            print("Optimal solution found --- Simplex Algorithm successfully terminated")
        else:
            print("Max iterations reached")