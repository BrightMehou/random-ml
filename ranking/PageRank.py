#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 21:33:23 2024

@author: jmehou  & yananga
"""

### TP de Big Data

import numpy as np
import scipy.linalg as nla
import pandas as pd
import matplotlib.pyplot as plt
#%% Importation de la matrice d'adjacence

matrice_ad = pd.read_csv("matrice_ad.csv")
id_site = matrice_ad["Unnamed: 0"].to_list() # la liste des noms de page de la matrice
id_site.append("Virtual node NULL")
matrice_ad = matrice_ad.drop(["Unnamed: 0"], axis=1)
matrice_ad = matrice_ad.to_numpy()

#%% Constructioon de la matrice 

# Crée un noeud viruel NULL  relier aux noeuds terminaux du graphe
def handle_row_zeros(mat):
    sum_row = np.sum(mat, axis=1)
    n = mat.shape[0]
    res = np.zeros((n+1,n+1))
    res[:n,:n ]= mat.copy()
    for i in range(n):
        if  sum_row[i] == 0:
            res[i,n] = 1
            res[n,i] = 1
    return res 
         
# Retourne le matrice de transition P associée à la matrice d'adjacence
def matrice_transition(mat):
    res = handle_row_zeros(mat)
    return (1 / np.sum(res, axis=1)) * np.transpose(res)

#%%  Algorithme du PageRank

# Applique l'algorithme du PageRank à une matrice de transition P donnée en appliquant la méthode de la puissance
# personalized_nodes contient la liste des noeuds cibles pour exécuter le personalised PageRank
# Si personalized_nodes est vide c'est l'algorithme du PageRank basique qui est utilisé
def PageRank(P, personalized_nodes = [], beta = 0.85, epsilon = 1e-10):
    N = P.shape[0]
    L = len(personalized_nodes)
    if L == 0:
        q0 = (1 / np.sqrt(N)) * np.ones(N)
        v = np.ones(N)
        L = N
    else: 
        v = np.zeros(N)
        for node in personalized_nodes:
            v[node] = 1 
        q0 = v
    error = 1
    while error > epsilon:
        q1 = beta * np.dot(P, q0) 
        q1 = q1 + ((1 - beta) / L) * np.sum(q0) * v
        q1 = (1 / nla.norm(q1, 1)) * q1
        error = nla.norm(q1 - q0, 2)
        q0 = q1
    return q0   


#%% Résultats des classement

# Prend en paramètre la liste des noms de site web id_site et le vecteur retourner par la fonction PageRank ranking

# Associe chaque site a son score PageRank et les tris par ordre décroisant
def liste_ranking(id_site,ranking):
    n = len(id_site) + 1
    resultat = {"id_site" : id_site,
                "ranking" : ranking}
    resultat = pd.DataFrame(resultat)
    resultat = resultat.sort_values(by="ranking", ascending=False)
    resultat.insert(0, "classement", [i for i in range(1,n)])
    return resultat

# Résultats du PageRank et du personalised Pagerank

P = matrice_transition(matrice_ad)
ranking = PageRank(P,beta=0.85)
perso_ranking = PageRank(P, personalized_nodes=[108],beta=0.85) 
ranking = liste_ranking(id_site, ranking)
perso_ranking = liste_ranking(id_site, perso_ranking)

# Résultats du  reverse PageRank et du  reverse personalised Pagerank

matrice_ad_T = np.transpose(matrice_ad)
P_reverse = matrice_transition(matrice_ad_T)
reverse_ranking = PageRank(P_reverse ,beta=0.85)
reverse_ranking_perso = PageRank(P_reverse , personalized_nodes=[190,22],beta=0.85)
reverse_ranking = liste_ranking(id_site, reverse_ranking)
reverse_ranking_perso = liste_ranking(id_site ,reverse_ranking_perso)
#%% Enregistrer sous format CSV dans un fichier

save = ranking # le data frame que l'on souhaite enregister
save.to_csv("résultat ranking",index=False )
#%% Analyse de la complexité

# Cette fonction effectue les mêmes tâches que la fonction PageRank sauf qu'elle retourne le nombre d'itération avant convergence de l'algorithme
def PageRank_nb_op(P, personalized_nodes = [], beta = 0.85, epsilon = 1e-10):
    N = P.shape[0]
    L = len(personalized_nodes)
    if L == 0:
        q0 = (1 / np.sqrt(N)) * np.ones(N)
        v = np.ones(N)
        L = N
    else: 
        v = np.zeros(N)
        for node in personalized_nodes:
            v[node] = 1 
        q0 = v
    error = 1
    nb = 0
    while error > epsilon:
        q1 = beta * np.dot(P, q0) 
        q1 = q1 + ((1 - beta) / L) * np.sum(q0) * v
        q1 = (1 / nla.norm(q1, 1)) * q1
        error = nla.norm(q1 - q0, 2)
        q0 = q1
        nb = nb + 1 
    return nb  

    
beta = np.linspace(0.05, 0.95,10)
nb_op_page_rank = [PageRank_nb_op(P,beta=x) for x in beta]
nb_op_page_rank_perso = [PageRank_nb_op(P,personalized_nodes=[20,468],beta=x) for x in beta]
nb_op_reverse = [PageRank_nb_op(P_reverse ,beta=x) for x in beta]
nb_op_reverse_perso = [PageRank_nb_op(P_reverse ,personalized_nodes=[58],beta=x) for x in beta]

#%% Tracé des courbes

plt.plot(beta,nb_op_page_rank, label = "PageRank", color ="b")
plt.plot(beta,nb_op_page_rank_perso, label = "Personalised PageRank", color="r" )
plt.plot(beta,nb_op_reverse, label = "Reverse PageRank" , color ="g" )
plt.plot(beta,nb_op_reverse_perso, label = "Personalised Reverse PageRank", color = "orange")
plt.title("Résultats epsilon = 1e-10")
plt.xlabel("Damping factor beta")
plt.ylabel("Nombre d'itérations")
plt.xticks(np.arange(0, 1.01,0.1 ))
plt.yticks(np.arange(0, 410, 100))
plt.grid()
plt.legend()
plt.show()
