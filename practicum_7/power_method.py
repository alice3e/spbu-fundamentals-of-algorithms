import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat


def power_method(A: NDArrayFloat, n_iters: int) -> tuple[NDArrayFloat, NDArrayFloat]: # возвращаем историю поиска доминирующего собственного числа
    print(A)
    dominant_eigenvector_list = np.zeros((n_iters, len(A[0])))
    dominant_eigennumber_list = np.zeros(n_iters,)
    
    u_k = np.random.random(A.shape[0])
    u_kk = np.zeros_like(u_k)
    for k in range(n_iters):
        pre_u_kk = A @ u_k
        A_u_k_norm = np.linalg.norm(pre_u_kk)
        u_kk = pre_u_kk / A_u_k_norm
        dominant_eigenvalue = A_u_k_norm * u_kk[0] / u_k[0]
        u_k = u_kk
        dominant_eigennumber_list[k] = dominant_eigenvalue
        dominant_eigenvector_list[k] = u_kk
    
    return dominant_eigennumber_list, dominant_eigenvector_list

if __name__ == "__main__":
    V = np.array( # матрциа собсвтенных векторов
        [
            [1.0, 0.0, -1.0],
            [-1.0, 1.0, 1.0],
            [3.0, -1.0, -2.0],
        ]
    ) 
    dominant_eigenvalue_values = [3.0, 2.1] # домиминируещее собственное число
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    n_iters = 100
    for e in dominant_eigenvalue_values:
        L = np.diag([e, -2.0, 1.0])
        A = V @ L @ np.linalg.inv(V)
        eigenvalue_history, eigenvector_history = power_method(A, n_iters=n_iters)
        ax.semilogy(
            range(n_iters),
            np.abs(eigenvalue_history - L[0, 0]),
            "o--",
            label=f"Convergence rate: {np.abs(e / L[1, 1])}",
        )
    ax.grid()
    ax.legend(fontsize=12)
    ax.set_xlabel("Iteration", fontsize=12)
    ax.set_ylabel(r"$|\hat{\lambda} - \lambda|$", fontsize=12)
    plt.show()
