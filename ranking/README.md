# Info:

Successful (i.e., finished) Wikispeedia paths.
Article names are URL-encoded; e.g., in Java they can be decoded using java.net.URLDecoder.decode(articleName, "UTF-8").
Articles in a path are separated by ";".
Back clicks are represented as "<".
Ratings are optionally given by the user after finishing the game and range from 1 ("easy") to 5 ("brutal").
Missing ratings are represented as "NULL".
FORMAT:   hashedIpAddress   timestamp   durationInSec   path   rating
When publishing on this data set, please cite:
(1) Robert West and Jure Leskovec:
Human Wayfinding in Information Networks.
21st International World Wide Web Conference (WWW), 2012.
(2) Robert West, Joelle Pineau, and Doina Precup:
Wikispeedia: An Online Game for Inferring Semantic Distances between Concepts.
21st International Joint Conference on Artificial Intelligence (IJCAI), 2009.


### Fichier TSV : "paths_finished.tsv"

Ce fichier est un jeu de données qui comporte des chemins de navigation à
étudier.

### Fichier R Markdown : "Prétraitement.Rmd"

Ce fichier :
  - importe les données du fichier "paths_finished.tsv"
  - effectue le nettoyage des données en supprimant les chemins de navigation
  doublons, puis en les formatant en paires de noeuds (arêtes du graphe)
  - construit le graphe à partir des connexions entre les noeuds
  - génère et sauvegarde la matrice d'adjacence associée au graphe dans un
  fichier "matrice_ad.csv". Ce fichier sera par la suite utilisé pour appliquer
  les méthodes PageRank vues en cours.
  
### Fichier Python : "PageRank.py"

Ce fichier :
  - importe la matrice d'adjacence à partir du fichier "matrice_ad.csv" évoqué
  précédemment
  - construit une matrice de transition à partir de la matrice d'adjacence
  - implémente les quatre méthodes PageRank (PR, PPR : personnalisé
  RPR : Reverse, PRPR : Reverse personnalisé)
  - effectue les classements, basés sur chacune de ces méthodes, des pages web
  présentes dans le jeu de données
  - enregistre les résultats dans des fichiers CSV
  - trace les courbes montrant le nombre d'itérations nécessaires pour la
  convergence de chacune des méthodes PageRank étudiées, en fonction du facteur
  de téléportation (Damping factor) beta, pour différentes conditions
  expérimentales


## Instructions pour exécuter le projet :

- Décompresser l'archive et accéder au répertoire où celle-ci a été décompressée
- Ouvrir le fichier "Prétraitement.Rmd" (il faudrait disposer au préalable de
Rstudio ou de tout autre environnement de travail R)
- Exécuter chaque *chunk* dans leur ordre d'apparition dans le code, ou
les exécuter en une fois en cliquant sur "Run" puis "Run All" (ou simplement
**Ctrl + Alt + R** en raccourci clavier)
-(Le fichier "matrice_ad.csv" a normalement été créé dans le répertoire courant)
- Ouvrir le fichier "PageRank.py" (il faudrait disposer au préalable de Spyder
en plus de Python 3)
- Modifier les lignes du code dédiées à l'enregistrement des résultats. Elles
sont présentes à la toute fin de la portion de code "Résultats du Reverse
PageRank et du reverse personalised PageRank".
  EXEMPLE : save = *nom_méthode_PageRank*_ranking(/ranking_perso)
            save.to_csv(*votre_nom_de_fichier*, index=False)
  avec *nom_méthode_PageRank* = *reverse*, *perso* ...
- Exécuter tout le code (L'exécution risque de prendre un peu de temps... Soyez
patients)
-(En fait, une exécution entière du code est requise avant d'exécuter les portions
sans bug)
-(Normalement, un fichier CSV est créé et présent dans votre répertoire courant)
- Vous pouvez, après cette première exécution, exécuter chaque portion de code
sans souci. Ainsi, vous pouvez enregistrer plusieurs fichiers pour les différentes
méthodes PageRank utilisées sans que cela ne prenne beaucoup de temps à chaque fois.
- Le graphe comportant les courbes générées à l'analyse de la complexité sont
normalement disponibles dans la section "Plots" (de Spyder)
- Vous pouvez bien sûr définir votre propre liste de noeuds personnalisés si vous
souhaitez appliquer une méthode PageRank personnalisée en modifiant le paramètre
*personalized_nodes*