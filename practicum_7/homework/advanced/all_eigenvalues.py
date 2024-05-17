from collections import defaultdict
from dataclasses import dataclass
import os
import yaml
import time


import numpy as np
import scipy.io
import scipy.linalg

from src.common import NDArrayFloat
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
    """
    Computes eigenvalues of a real square matrix using the QR algorithm with shifts.

    Args:
        A: The input real square matrix.
        tol: Tolerance for convergence.
        max_iter: Maximum number of iterations.

    Returns:
        eigenvalues: A 1D NumPy array containing the eigenvalues of A.
    """
    max_iter = 50
    n = A.shape[0]
    for _ in range(max_iter):
        # Apply shifts
        H = np.zeros((n, n))
        H[n-1, n-1] = A[n-1, n-1]
        shift = H[n-1, n-1]

        # QR decomposition with shifts (using your existing function)
        Q, R = qr_decomposition(A - shift * np.eye(n))

        # Update A
        A = np.dot(R, Q) + shift * np.eye(n)  # Apply the shift back

    eigenvalues = np.diag(A).copy()
    return eigenvalues

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
