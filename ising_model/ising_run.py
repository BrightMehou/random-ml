from numba import njit, prange
import numpy as np
import time
import matplotlib.pyplot as plt

@njit
def create_Materiaux(N):
    shape = 2 * N + 1
    mat = np.ones((shape, shape), dtype=np.int8)
    for i in range(1, shape - 1):
        for j in range(1, shape - 1):
            if np.random.rand() > 0.5:
                mat[i, j] = 1
            else:
                mat[i, j] = -1
    return mat

@njit(parallel=True)
def simulation_ising(converge, sim, N, Tmin, Tmax, nb_point):
    temp_list = np.linspace(Tmin, Tmax, nb_point)
    esp_resultats = np.zeros(nb_point)
    L = 2 * N + 1 

    for j in prange(nb_point):
        T = temp_list[j]

        p4 = np.exp(-4.0 / T)
        p8 = np.exp(-8.0 / T)
        
        mat = create_Materiaux(N)
        
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

# --- Paramètres de simulation ---
N = 100
converge = 10**9 
sim = converge
Tmin = 0.5
Tmax = 4.0
nb_point = 25

print(f"Lancement de la simulation (N={N}, itérations={sim})...")
start = time.perf_counter()

temp, esperance = simulation_ising(converge, sim, N, Tmin, Tmax, nb_point)

duree = round(time.perf_counter() - start)
print(f"Simulation terminée en {duree} secondes.")

# --- Visualisation ---
plt.figure(figsize=(10, 6))
plt.plot(temp, esperance, 'o-', label=f'N={N}')
plt.axvline(x=2.269, color='r', linestyle='--', label='Tc ≈ 2.27 (Théorique)')
plt.title(f"Transition de phase : $E_{{N,T}}^+[\sigma(0)]$ (sim={sim})")
plt.xlabel("Température (T)")
plt.ylabel("Espérance du spin à l'origine")
plt.legend()
plt.grid(True)
plt.show()