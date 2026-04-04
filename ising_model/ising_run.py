from numba import njit, prange
import numpy as np
import time
import matplotlib.pyplot as plt

@njit
def create_Materiaux(N, mode=1):
    shape = 2 * N + 1
    mat = np.full((shape, shape), np.int8(mode))
    n = shape - 1
    for i in range(1,n):
        for j in range(1,n):
            mat[i, j] = np.int8(1) if np.random.rand() > 0.5 else np.int8(-1)
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
def delta_energie(mat, i, j):
    # Lecture directe des voisins — les bords fixes sont déjà dans la matrice
    voisins = (mat[i-1, j] + mat[i+1, j] +
               mat[i, j-1] + mat[i, j+1])
    return 2 * mat[i, j] * voisins

@njit
def monte_carlo_iteration(mat, T):
    N = mat.shape[0] - 1
    a = np.random.randint(1, N)
    b = np.random.randint(1, N)

    dE = delta_energie(mat, a, b)
    # règle de Metropolis
    if dE <= 0 or np.random.rand() < np.exp(-dE / T):
        mat[a, b] *= -1

@njit(parallel=True)
def Ising(converge, sim, N, Tmin, Tmax, nb_point):
    temp = np.linspace(Tmin, Tmax, nb_point)
    esp = np.zeros(nb_point)

    for j in prange(nb_point):
        mat = create_Materiaux(N)
        for _ in range(converge):
            monte_carlo_iteration(mat, temp[j])
        # Loi forte des grands nombres pour les chaînes de Markov :
        acc = 0.0
        for _ in range(sim):
            monte_carlo_iteration(mat, temp[j])
            acc += mat[N, N]  

        esp[j] = acc / sim 

    return temp, esp

N = 20
converge =  10**9
sim = converge
Tmin = 0.1
Tmax = 4
nb_point = 10
mat = create_Materiaux(N)
start = time.perf_counter()
temp,simul = Ising(converge,sim,N,Tmin,Tmax,nb_point)
durée = round(time.perf_counter() - start)
plt.plot(temp,simul)
plt.title(f"N = {N}, sim ={sim}, time={durée}, points = {nb_point}")
plt.xlabel("Température")
plt.ylabel("Espérance à l'origine")
plt.xticks(np.arange(0, 4.1,0.3 ))
plt.yticks(np.arange(0, 1.1, 0.2))
plt.grid()
plt.show()