from simplxed import functions
from simplxed.functions import LP
import numpy as np
import pytest

def test_is_canonical_true():
    c_1 = [-4, -3]
    A_1 = [
         [2, 3],
         [-3, 2],
         [0, 2],
         [2, 1]
        ]
    b_1 = [6, 3, 5, 4]
    c_2 = [2, 3, 4]
    A_2 = [
         [3, 2, 1],
         [2, 5, 3]
        ]
    b_2 = [10, 15]
    assert ((functions.is_canonical(c_1, A_1, b_1)==True) and
            (functions.is_canonical(c_1, A_1, b_1)==True)
        )

def test_is_canonical_false():
    c_1 = [-4, -3]
    A_1 = [
         [2, 3],
         [-3, 2]
        ]
    b_1 = [6, 3, 5, 4]
    c_2 = [2, 3, 4]
    A_2 = [
         [3, 2, 1],
         [2, 5, 3]
        ]
    b_2 = [10, -15]
    assert ((functions.is_canonical(c_1, A_1, b_1)==False) and 
            (functions.is_canonical(c_1, A_1, b_1)==False) and
            (functions.is_canonical([],[],[])==False)
        )

def test_to_tableau():
    c_1 = [-4, -3]
    A_1 = [
         [2, 3],
         [-3, 2],
         [0, 2],
         [2, 1]
        ]
    b_1 = [6, 3, 5, 4]
    ctab_1 = np.array([
        [1, -4, -3, 0, 0, 0, 0, 0],
        [0,  2,  3, 1, 0, 0, 0, 6],
        [0, -3,  2, 0, 1, 0, 0, 3],
        [0,  0,  2, 0, 0, 1, 0, 5],
        [0,  2,  1, 0, 0, 0, 1, 4]
    ], dtype=float)
    c_2 = [2, 3, 4]
    A_2 = [
         [3, 2, 1],
         [2, 5, 3]
        ]
    b_2 = [10, 15]
    ctab_2 = np.array([
        [1, 2, 3, 4, 0, 0,  0],
        [0, 3, 2, 1, 1, 0, 10],
        [0, 2, 5, 3, 0, 1, 15]
    ], dtype=float)
    assert (np.array_equal(functions.to_tableau(c_1, A_1, b_1), ctab_1) and
            np.array_equal(functions.to_tableau(c_2, A_2, b_2), ctab_2)
    )

def test_lp_class_inst():
    c_1 = [2, 3, 4]
    A_1 = [
         [3, 2, 1],
         [2, 5, 3]
        ]
    b_1 = [10, 15]
    ctab = np.array([
        [1, 2, 3, 4, 0, 0,  0],
        [0, 3, 2, 1, 1, 0, 10],
        [0, 2, 5, 3, 0, 1, 15]
    ], dtype=float)
    c_2 = [2, 3, 4]
    A_2 = [
         [3, 2, 1],
         [2, 5, 3]
        ]
    b_2 = [10, -15]
    lp1 = LP(c_1,A_1,b_1)
    assert(np.array_equal(lp1.tab,ctab))
    with pytest.raises(ValueError):
        lp2 = LP(c_2,A_2,b_2)