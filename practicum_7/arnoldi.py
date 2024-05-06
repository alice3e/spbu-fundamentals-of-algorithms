import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat
from qr import get_eigenvalues_via_qr

def get_arnoldi_vectors(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:
    n = len(A[0])
    Q = np.zeros((n,n_iters))
    v_k = np.random.rand (n)
    u_k = v_k / np.linalg.norm(v_k)
    Q[: , 0] = u_k
    for k in range(1,n_iters):
        u_k = Q[: , k-1]
        v_kk = A @ Q[: , k-1]
        for j in range(k):
            u_j = Q[:, j]
            h_jk = np.dot(v_kk, u_j)
            v_kk -= h_jk * u_j
        Q[: , k] = v_kk / np.linalg.norm(v_kk)
    return Q


if __name__ == "__main__":
    A = np.array(
        [
            [4.0, 1.0, -1.0, 2.0],
            [1.0, 4.0, 1.0, -1.0],
            [-1.0, 1.0, 4.0, 1.0],
            [2.0, -1.0, 1.0, 1.0],
        ]
    )

    Q = get_arnoldi_vectors(A, n_iters=3)
    print(Q)
    lambd = Q[: , 0] @ Q[:,1]
    print(lambd) # показали что ортонормированы
    
    lambdas = get_eigenvalues_via_qr(Q,10)
    print(lambdas)
    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    # computing eigenvalues...
