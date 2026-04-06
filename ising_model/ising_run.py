from numba import njit, prange
import numpy as np
import time
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

@njit
def create_Materiaux(N: int, mode: int) -> np.ndarray:
    shape = 2 * N + 1
    mat = np.full((shape, shape), mode, dtype=np.int8)
    for i in range(1, shape - 1):
        for j in range(1, shape - 1):
            if np.random.rand() > 0.5:
                mat[i, j] = 1
            else:
                mat[i, j] = -1
    return mat

@njit(parallel=True)
def simulation_ising(converge: int, sim: int, N: int, Tmin: float, Tmax: float, nb_point: int, mode: int = 1) -> tuple[np.ndarray, np.ndarray]:
    temp_list = np.linspace(Tmin, Tmax, nb_point)
    esp_resultats = np.zeros(nb_point)
    L = 2 * N + 1 

    for j in prange(nb_point):
        T = temp_list[j]

        p4 = np.exp(-4.0 / T)
        p8 = np.exp(-8.0 / T)
        
        mat = create_Materiaux(N, mode)
        
        for _ in range(converge):
            a = np.random.randint(1, L - 1)
            b = np.random.randint(1, L - 1)
            
            voisins = mat[a-1, b] + mat[a+1, b] + mat[a, b-1] + mat[a, b+1]
            dE = 2 * mat[a, b] * voisins
        
            if dE <= 0:
                mat[a, b] *= -1
            elif dE == 4:
                if np.random.rand() < p4:
                    mat[a, b] *= -1
            elif dE == 8:
                if np.random.rand() < p8:
                    mat[a, b] *= -1

        # Phase de mesure (Loi forte des grands nombres)
        acc = 0.0
        for _ in range(sim):
            a = np.random.randint(1, L - 1)
            b = np.random.randint(1, L - 1)
            voisins = mat[a-1, b] + mat[a+1, b] + mat[a, b-1] + mat[a, b+1]
            dE = 2 * mat[a, b] * voisins
            
            if dE <= 0:
                mat[a, b] *= -1
            elif dE == 4:
                if np.random.rand() < p4:
                    mat[a, b] *= -1
            elif dE == 8:
                if np.random.rand() < p8:
                    mat[a, b] *= -1
            
            acc += mat[N, N]

        esp_resultats[j] = acc / sim 

    return temp_list, esp_resultats

if __name__ == "__main__":
    N = 25
    converge = 10**7 
    sim = converge
    Tmin = 0.5
    Tmax = 4.0
    nb_point = 25
    mode = -1
    logger.info(f"Lancement de la simulation {N=}, {sim=}, {mode=}...")
    start = time.perf_counter()

    temp, esperance = simulation_ising(converge, sim, N, Tmin, Tmax, nb_point, mode)

    duree = round(time.perf_counter() - start)
    logger.info(f"Simulation terminée en {duree} secondes.")

    plt.figure(figsize=(10, 6))
    plt.plot(temp, esperance, 'o-', label=f'N={N}')
    plt.axvline(x=2.269, color='r', linestyle='--', label='Tc ≈ 2.27 (Théorique)')
    plt.title(f"Transition de phase: {sim=}, {mode=}")
    plt.xlabel("Température (T)")
    plt.ylabel("Espérance du spin à l'origine")
    plt.legend()
    plt.grid(True)
    plt.show()