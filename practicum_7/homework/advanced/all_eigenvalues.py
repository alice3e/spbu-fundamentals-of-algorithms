from collections import defaultdict
from dataclasses import dataclass
import os
import yaml
import time


import numpy as np
import scipy.io
import scipy.linalg

# ---
from collections import namedtuple
from numpy.typing import NDArray
ProblemCase = namedtuple("ProblemCase", "input, output")
NDArrayInt = NDArray[np.int_]
NDArrayFloat = NDArray[np.float_]
# ---

from src.linalg import get_numpy_eigenvalues


@dataclass
class Performance:
    time: float = 0.0
    relative_error: float = 0.0

def qr_decomposition(A: np.array):
    """
    Optimized Gram-Schmidt process with normalization.
    The coefficients q will be calculated at each step of the algorithm.
    Each time we will subtract the component of the vector from all the vectors q at once.
    """
    m, n = A.shape  # Get both dimensions of A
    Q = A.copy()
    R = np.zeros((n, n))  # Initialize R with zeros

    for k in range(n): # Orthogonalize the k-th column
        R[k, k] = np.linalg.norm(Q[:, k]) # Normalize the k-th column
        Q[:, k] /= R[k, k] 
        for j in range(k + 1, n): # Subtract the projection from subsequent columns 
            R[k, j] = np.dot(Q[:, k], Q[:, j])
            Q[:, j] -= R[k, j] * Q[:, k] 
    return Q, R


def get_all_eigenvalues(A: NDArrayFloat) -> NDArrayFloat:
    print("starting")
    A_k = A.copy()
    for k in range(100):
        Q,R = qr_decomposition(A_k)
        A_k = R @ Q
    my_eigenvalues = np.array(np.diag(A_k))
    return my_eigenvalues
    
# Result summary:
# Matrix: bp__1000.mtx.gz. Average time: 1.21e+02 seconds. Relative error: 7.88e-01
# Matrix: e05r0100.mtx.gz. Average time: 8.20e+00 seconds. Relative error: 7.82e-02
# Matrix: fs_541_1.mtx.gz. Average time: 4.91e+01 seconds. Relative error: 4.09e-04
# Matrix: fs_680_1.mtx.gz. Average time: 7.75e+01 seconds. Relative error: 1.39e-08
# Matrix: gre_1107.mtx.gz. Average time: 2.59e+02 seconds. Relative error: 7.27e-01
# Matrix: hor__131.mtx.gz. Average time: 3.16e+01 seconds. Relative error: 4.26e-01
# Matrix: impcol_c.mtx.gz. Average time: 2.62e+00 seconds. Relative error: 6.52e-01
# Matrix: impcol_d.mtx.gz. Average time: 3.05e+01 seconds. Relative error: 8.21e-01
# Matrix: impcol_e.mtx.gz. Average time: 7.46e+00 seconds. Relative error: 7.61e-01
# Matrix: jpwh_991.mtx.gz. Average time: 2.10e+02 seconds. Relative error: 2.02e-03
# Matrix: lns__511.mtx.gz. Average time: 4.51e+01 seconds. Relative error: 9.01e-01
# Matrix: mahindas.mtx.gz. Average time: 3.61e+02 seconds. Relative error: 8.74e-01
# Matrix: mcca.mtx.gz. Average time: 4.54e+00 seconds. Relative error: 8.35e-02
# Matrix: mcfe.mtx.gz. Average time: 1.01e+02 seconds. Relative error: 5.10e-02
# Matrix: nos5.mtx.gz. Average time: 3.52e+01 seconds. Relative error: 4.30e-03
# Matrix: orsirr_1.mtx.gz. Average time: 2.16e+02 seconds. Relative error: 3.91e-02

def run_test_cases(
    path_to_homework: str, path_to_matrices: str
) -> dict[str, Performance]:
    matrix_filenames = []
    performance_by_matrix = defaultdict(Performance)
    with open(os.path.join(path_to_homework, "matrices.yaml"), "r") as f:
        matrix_filenames = yaml.safe_load(f)
    for i, matrix_filename in enumerate(matrix_filenames):
        print(f"Processing matrix {i+1} out of {len(matrix_filenames)}")
        A = scipy.io.mmread(os.path.join(path_to_matrices, matrix_filename)).todense().A
        perf = performance_by_matrix[matrix_filename]
        t1 = time.time()
        eigvals = get_all_eigenvalues(A)
        eigvals_exact = get_numpy_eigenvalues(A)
        t2 = time.time()
        perf.time += t2 - t1
        eigvals_exact.sort()
        eigvals.sort()
        relative_error = np.median(
            np.abs(eigvals_exact - eigvals) / np.abs(eigvals_exact)
        )
        perf.relative_error = relative_error
        print("matrix summary:")
        print(
            f"Matrix: {matrix_filename}. "
            f"Average time: {(t2 - t1):.2e} seconds. "
            f"Relative error: {relative_error:.2e}"
        )
    return performance_by_matrix


if __name__ == "__main__":
    path_to_homework = os.path.join("practicum_7", "homework", "advanced")
    path_to_matrices = os.path.join("practicum_6", "homework", "advanced", "matrices")
    performance_by_matrix = run_test_cases(
        path_to_homework=path_to_homework,
        path_to_matrices=path_to_matrices,
    )

    print("\nResult summary:")
    for filename, perf in performance_by_matrix.items():
        print(
            f"Matrix: {filename}. "
            f"Average time: {perf.time:.2e} seconds. "
            f"Relative error: {perf.relative_error:.2e}"
        )


