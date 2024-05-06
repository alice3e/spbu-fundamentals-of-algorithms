import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat


# def qr(A: NDArrayFloat) -> tuple[NDArrayFloat, NDArrayFloat]: # на выходе Q и R
#     n = A.shape[0]
#     print(A)
#     print("~"*15)
#     Q = np.zeros_like(A)
#     R = np.zeros_like(A)
#     for i in range(n):
#         v = A[:, i]
#         for j in range(i):
#             R[j, i] = np.dot(Q[:, j], A[:, i]) # скалярное умножение
#             v = v - R[j, i] * Q[:, j] 
#         R[i, i] = np.linalg.norm(v)
#         Q[:, i] = v / R[i, i]
#     return Q, R
    
def qr(A: NDArrayFloat) -> tuple[NDArrayFloat, NDArrayFloat]: # на выходе Q и R
    n = A.shape[0]
    Q = np.zeros_like(A)
    R = np.zeros_like(A)
    W = A.copy()
    
    for j in range(n):
        w_j_norm = np.linalg.norm(W[: , j])
        Q[: , j ] = W[: , j] / w_j_norm # W[: , j] == w_j^j
        for i in range(j):
            R[i,j] = A[: , j] @ Q[:, i]
        a_j_norm = np.linalg.norm(A[:, j])
        R[j,j] = np.sqrt(a_j_norm**2 - np.sum(R[ :j , j] ** 2))
        for k in range(j+1,n):
            prod = W[: , k] @ Q[: , j]
            W[:, k ] = W[: , k] - prod * Q[:, j]
    return Q,R

def get_eigenvalues_via_qr(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:
    A_k = A.copy()
   
    for k in range(n_iters):
        Q, R = qr(A_k)
        A_k = R @ Q
    return np.diag(A_k)


def householder_tridiagonalization(A: NDArrayFloat) -> NDArrayFloat: # случай для диагональных матриц -> сходимость улучшаем
    n = len(A[0])
    A_triag = A.copy()
    for i in range(n-2):
        x = np.zeros(n)
        x[i+1:] = A_triag[i + 1 : , i]
        y = np.zeros(n)
        y[i + 1] = np.linalg.norm(x)
        if(x[i+1] * y[i+1] > 0 ): y[i+1] *= 1
        u = (x - y) / (np.linalg.norm(x - y))
        H = np.eye(n) - 2*(np.outer(u,u)) # внешнее произведение
        A_triag = H @ A_triag @ H
        
    for i in range(n):
        for j in range(n):
            if(A_triag[i][j] < 10e-13): A_triag[i][j] = 0
    print(A_triag)
    return A_triag




def sign(x):
    return 1 if x > 0 else -1


if __name__ == "__main__":
    A = np.array(
        [
            [4.0, 1.0, -1.0, 2.0],
            [1.0, 4.0, 1.0, -1.0],
            [-1.0, 1.0, 4.0, 1.0],
            [2.0, -1.0, 1.0, 1.0],
        ]
    )
    #Q,R = qr(A)
    #print(Q @ R)
    #eigvals = get_eigenvalues_via_qr(A, n_iters=20)
    #print(eigvals)
    A_tri = householder_tridiagonalization(A)
    eigvals_tri = get_eigenvalues_via_qr(A_tri, n_iters=20)
    print(eigvals_tri)
