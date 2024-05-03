import numpy as np
import scipy.linalg


def get_scipy_solution(A, b):
    lu_and_piv = scipy.linalg.lu_factor(A)
    return scipy.linalg.lu_solve(lu_and_piv, b)
