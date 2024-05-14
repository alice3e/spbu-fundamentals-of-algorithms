import os
from typing import Optional

import numpy as np
from numpy.typing import DTypeLike
import scipy.io
import matplotlib.pyplot as plt

from src.common import NDArrayFloat
from src.linalg import get_scipy_solution


def conjugate_gradient_method(
    A: NDArrayFloat,
    b: NDArrayFloat,
    n_iters: Optional[int] = None,
    dtype: Optional[DTypeLike] = None,
) -> NDArrayFloat:

    solution_history = np.zeros((n_iters, A.shape[0]), dtype=dtype)
    
    x_k = np.zeros(A.shape[0])
    r_k = b - (A @ x_k)
    v_k = r_k.copy()
    
    for k in range(n_iters):
        t_k = np.dot(r_k, r_k) / np.dot(v_k, A @ v_k)
        x_k = x_k + t_k * v_k
        solution_history[k] = x_k
        r_k_p = r_k.copy()
        r_k = r_k - t_k * A @ v_k
        s_k = np.dot(r_k, r_k) / np.dot(r_k_p, r_k_p)
        v_k = r_k + s_k * v_k

    return solution_history


def preconditioned_conjugate_gradient_descent(
    A: NDArrayFloat,
    b: NDArrayFloat,
    C_inv: NDArrayFloat,
    n_iters: Optional[int] = None,
    dtype: Optional[DTypeLike] = None,
) -> NDArrayFloat:

    solution_history = np.zeros((n_iters, A.shape[0]), dtype=dtype)
    
    x_k = np.zeros(A.shape[0])
    r_k = b - (A @ x_k)
    w_k = C_inv @ r_k
    v_k = C_inv.T @ w_k
    for k in range(n_iters):
        t_k = np.dot(w_k, w_k) / np.dot(v_k, A @ v_k)
        x_k = x_k + t_k * v_k
        solution_history[k] = x_k
        r_k = r_k - t_k * A @ v_k
        w_k_p = w_k.copy()
        w_k = C_inv @ r_k
        s_k = np.dot(w_k, w_k) / np.dot(w_k_p, w_k_p)
        v_k = C_inv.T @ w_k + s_k * v_k

    return solution_history


def relative_error(x_true, x_approx):
    return np.linalg.norm(x_true - x_approx, axis=1) / np.linalg.norm(x_true)


def add_convergence_graph_to_axis(
    ax, exact_solution: NDArrayFloat, solution_history: NDArrayFloat
) -> None:
    n_iters = solution_history.shape[0]
    ax.semilogy(
        range(n_iters),
        relative_error(x_true=exact_solution, x_approx=solution_history),
        "o--",
    )
    ax.grid()
    ax.legend(fontsize=12)
    ax.set_xlabel("Iteration", fontsize=12)
    ax.set_ylabel(r"$||x - \tilde{x}|| / ||x||$", fontsize=12)


if __name__ == "__main__":
    np.random.seed(42)

    # Try the following matrices
    # nos5.mtx.gz (pos.def., K = O(10^4))
    # bcsstk14.mtx.gz (pos.def., K = O(10^10))

    path_to_matrix = os.path.join(
        "practicum_6", "homework", "advanced", "matrices", "nos5.mtx.gz"
    )
    A = scipy.io.mmread(path_to_matrix).todense().A

    b = np.ones((A.shape[0],))
    exact_solution = get_scipy_solution(A, b)
    n_iters = 1000

    # Convergence speed for the conjugate gradient method
    solution_history = conjugate_gradient_method(A, b, n_iters=n_iters)

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    add_convergence_graph_to_axis(ax, exact_solution, solution_history)
    plt.show()

    # Convergence speed for the preconditioned conjugate gradient method

    C_inv = np.diag(1.0 / np.sqrt(np.diag(A))) # матрица  C^{-1}
    A_tilde = C_inv @ A @ C_inv # число конфликтов снижается в 10e7 раз
    
    
    solution_history = preconditioned_conjugate_gradient_descent(
        A, b, C_inv, n_iters=n_iters
    )

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    add_convergence_graph_to_axis(ax, exact_solution, solution_history)
    plt.show()

    print()
