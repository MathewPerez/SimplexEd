from simplxed import functions
from simplxed.functions import LP
import numpy as np
import pytest

# Define globals for testing
c_1 = [-4, -3]
A_1 = [
        [2, 3],
        [-3, 2],
        [0, 2],
        [2, 1]
    ]
b_1 = [6, 3, 5, 4]

c_2 = [-2, -3, -4]
A_2 = [
        [3, 2, 1],
        [2, 5, 3]
    ]

c_3 = [-20, -12, -40, -25]
A_3 = [[1, 1, 1, 1],
        [3, 2, 1, 0],
        [0, 1, 2, 3]]
b_3 = [ 50,
        100,
        90]

b_2 = [10, 15]

A_1_f = [
         [2, 3],
         [-3, 2]
        ]
b_2_f = [10, -15]

ctab_1 = np.array([
    [1, -4, -3, 0, 0, 0, 0, 0],
    [0,  2,  3, 1, 0, 0, 0, 6],
    [0, -3,  2, 0, 1, 0, 0, 3],
    [0,  0,  2, 0, 0, 1, 0, 5],
    [0,  2,  1, 0, 0, 0, 1, 4]
], dtype=float)

ctab_2 = np.array([
    [1, -2, -3, -4, 0, 0,  0],
    [0,  3,  2,  1, 1, 0, 10],
    [0,  2,  5,  3, 0, 1, 15]
], dtype=float)

ctab_1_piv = [
    [ 1,   0,    -1,   0,   0,   0,     2,   8 ],
    [ 0,   0,     2,   1,   0,   0,    -1,   2 ],
    [ 0,   0,   3.5,   0,   1,   0,   1.5,   9 ],
    [ 0,   0,     2,   0,   0,   1,     0,   5 ],
    [ 0,   1,   0.5,   0,   0,   0,   0.5,   2 ]
]

decode_ctab2 = np.array([
    [ 1.,          0.66666667,  3.66666667,  0.,          0.,          1.33333333,    20.   ],
    [ 0.,          2.33333333,  0.33333333,  0.,          1.,         -0.33333333,    5.    ],
    [ 0.,          0.66666667,  1.66666667,  1.,          0.,          0.33333333,    5.    ]
], dtype=float)

ctab1_sol = [1.5, 1.0, 0, 5.5, 3.0, 0, 9.0]

ctab2_sol = [0, 0, 5.0, 5, 0, 20.0]

ctab3_sol = [5.0, 0, 45.0, 0, 0, 40.0, 0, 1900.0]

#####################################
#####       Test Cases          #####
#####################################

def test_is_canonical_true():
    assert ((functions.is_canonical(c_1, A_1, b_1)==True) and
            (functions.is_canonical(c_1, A_1, b_1)==True)
        )

def test_is_canonical_false():
    assert ((functions.is_canonical(c_1, A_1_f, b_1)==False) and 
            (functions.is_canonical(c_2, A_2, b_2_f)==False) and
            (functions.is_canonical([],[],[])==False)
        )

def test_to_tableau():
    assert (np.array_equal(functions.to_tableau(c_1, A_1, b_1), ctab_1) and
            np.array_equal(functions.to_tableau(c_2, A_2, b_2), ctab_2)
    )

def test_lp_class_inst():
    lp1 = LP(c_1, A_1, b_1)
    assert(np.array_equal(lp1.tab,ctab_1))
    with pytest.raises(ValueError):
        lp2 = LP(c_2,A_2,b_2_f)

def test_decode():
    lp1 = LP(c_1, A_1, b_1)
    lp1.tab = decode_ctab2
    assert(lp1.decode()==ctab2_sol)

def test_getPivCol():
    lp1 = LP(c_1,A_1,b_1)
    lp1.getPivCol()
    lp2 = LP(c_2,A_2,b_2)
    lp2.getPivCol()
    assert(lp1.pcol==1 and 
           lp2.pcol==3
    )

def test_getPivRow():
    lp1 = LP(c_1,A_1,b_1)
    with pytest.raises(ValueError):
        lp1.getPivRow()
    lp1.getPivCol()
    lp1.getPivRow()
    lp2 = LP(c_2,A_2,b_2)
    lp2.getPivCol()
    lp2.getPivRow()
    assert(lp1.prow == 4 and
           lp2.prow == 2
    )

def test_pivot():
    lp1 = LP(c_1,A_1,b_1)
    lp1.getPivCol()
    with pytest.raises(ValueError):
        lp1.pivot()
    lp1.getPivRow()
    lp1.pivot()
    assert(np.array_equal(lp1.tab, ctab_1_piv))

def test_optimize():
    lp1 = LP(c_1,A_1,b_1)
    lp1.optimize()
    lp2 = LP(c_2,A_2,b_2)
    lp2.optimize()
    lp3 = LP(c_3,A_3,b_3)
    lp3.optimize()
    assert(
        (lp1.decode()==ctab1_sol) and
        (lp2.decode()==ctab2_sol) and
        (lp3.decode()==ctab3_sol)
    )