from collections import defaultdict
from dataclasses import dataclass
import os
import yaml
import time

import numpy as np
from numpy.typing import NDArray
import scipy.io
import scipy.linalg

from src.linalg import get_scipy_solution


@dataclass
class Performance:
    time: float = 0.0
    relative_error: float = 0.0


def lu(A: NDArray, permute: bool) -> tuple[NDArray, NDArray, NDArray]:
    n = A.shape[0]
    L = np.eye(n)
    U = np.copy(A)
    P = np.eye(n)

    for column in range(n-1):
        if(permute):
            max_index = np.argmax(abs(U[column:, column])) + column
            if max_index != column:
                U[[column, max_index]] = U[[max_index, column]]
                P[[column, max_index]] = P[[max_index, column]]
                if column != 0:
                    L[[column, max_index], :column] = L[[max_index, column], :column]
            
        a_diag_elem = U[column][column]
        for row in range(column + 1, n):
            coef = U[row][column] / a_diag_elem
            L[row][column] = coef
            #print(f'строка = {row} , столбец - {column}, | {U[row]} - {U[column] * coef}')
            U[row] -= (U[column] * coef)
    return L, U, P


def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:
    n = P.shape[0]
    x = np.zeros((n, 1))
    b_permuted = P.dot(b) # меняем местами стобцы b в соответствии с a
    
    # Обозначив вектор y как y = Ux мы находим его как решение уравнения: Ly = Pb = b_permutated
    y = np.zeros(n)
    for i in range(n):
        y[i] = b_permuted[i] -  (L[0:i+1 , 0:i+1] @ y[0:i+1])[i]
    
    # Ux = y
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.sum(U[i, i+1:] * x[i+1:])) / U[i, i]
    return x



def run_test_cases(n_runs: int, path_to_homework: str) -> dict[str, Performance]:
    matrix_filenames = []
    performance_by_matrix = defaultdict(Performance)
    with open(os.path.join(path_to_homework, "matrices.yaml"), "r") as f:
        matrix_filenames = yaml.safe_load(f)
    for i, matrix_filename in enumerate(matrix_filenames):
        print(f"Processing matrix {i+1} out of {len(matrix_filenames)}")
        A = (
            scipy.io.mmread(os.path.join(path_to_homework, "matrices", matrix_filename))
            .todense()
            .A
        )
        b = np.ones((A.shape[0],))
        perf = performance_by_matrix[matrix_filename]
        for j in range(n_runs):
            t1 = time.time()
            L, U, P = lu(A, permute=True)
            t2 = time.time()
            perf.time += t2 - t1
            if j == 0:  # first run => compute solution
                x = solve(L, U, P, b)
                x_exact = get_scipy_solution(A, b)
                perf.relative_error = np.linalg.norm(x - x_exact) / np.linalg.norm(x_exact)
    return performance_by_matrix


if __name__ == "__main__":
    n_runs = 1
    path_to_homework = os.path.join("practicum_6", "homework", "advanced")
    performance_by_matrix = run_test_cases(
        n_runs=n_runs, path_to_homework=path_to_homework
    )

    print("\nResult summary:")
    for filename, perf in performance_by_matrix.items():
        print(
            f"Matrix: {filename}. "
            f"Average time: {perf.time / n_runs:.2e} seconds. "
            f"Relative error: {perf.relative_error:.2e}"
        )