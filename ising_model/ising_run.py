from numba import njit, prange
import numpy as np
import time
import matplotlib.pyplot as plt

@njit
def create_Materiaux(N, mode=1):
    shape = 2 * N + 1
    mat = np.empty((shape, shape), dtype=np.int8)
    for i in range(shape):
        for j in range(shape):
            mat[i, j] = 1 if np.random.rand() > 0.5 else -1
    m = np.int8(mode)
    for i in range(shape):
        mat[0, i] = m
        mat[-1, i] = m
        mat[i, 0] = m
        mat[i, -1] = m
    return mat

@njit
def energie(mat):
    N = mat.shape[0]
    energ = 0
    for i in range(N):
        for j in range(N):
            energ += mat[i, j] * mat[i, (j + 1) % N]
            energ += mat[i, j] * mat[(i + 1) % N, j]
    return -energ

@njit
def monte_carlo_iteration(mat, T):
    N = mat.shape[0]
    a = np.random.randint(0, N)
    b = np.random.randint(0, N)

    e1 = energie(mat)
    mat[a, b] = -mat[a, b]   # tentative de flip
    e2 = energie(mat)

    dE = e2 - e1

    # règle de Metropolis
    if not (dE <= 0 or np.random.rand() < np.exp(-dE / T)):
        mat[a, b] = -mat[a, b]  # on annule le flip

@njit(parallel=True)
def Ising(converge, sim, N, Tmin, Tmax, nb_point):
    temp = np.linspace(Tmin, Tmax, nb_point)
    esp = np.zeros(nb_point)

    for j in prange(nb_point):
        mat = create_Materiaux(N)

        for _ in range(converge):
            monte_carlo_iteration(mat, temp[j])

        acc = 0.0
        for _ in range(sim):
            monte_carlo_iteration(mat, temp[j])
            acc += mat[N, N]  

        esp[j] = acc / (sim + 1)

    return temp, esp

N = 3
converge = 10**7
sim = converge
Tmin = 0.1
Tmax = 4
nb_point = 10
mat = create_Materiaux(N)
start = time.time()
temp,simul = Ising(converge,sim,N,Tmin,Tmax,nb_point)
durée = round(time.time() - start)
plt.plot(temp,simul)
plt.title(f"N = {N}, sim ={sim}, time={durée}, points = {nb_point}")
plt.xlabel("Température")
plt.ylabel("Espérance à l'origine")
plt.xticks(np.arange(0, 4.1,0.3 ))
plt.yticks(np.arange(0, 1.1, 0.2))
plt.grid()
plt.show()