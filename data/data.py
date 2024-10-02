import pandas as pd
import numpy as np

# Définition des paramètres pour la génération des données
np.random.seed(0)  # Pour rendre les résultats reproductibles
nb_projets = 1000
tailles_projet = np.random.randint(1, 1000, nb_projets)
complexites = np.random.choice(['Faible', 'Moyenne', 'Élevée'], nb_projets)
nb_ressources_humaines = np.random.randint(5, 50, nb_projets)
nb_ressources_materielles = np.random.randint(3, 20, nb_projets)
durees_projet = np.random.randint(3, 24, nb_projets)
risques = np.random.choice(['Faible', 'Modéré', 'Élevé'], nb_projets)
couts_projet = np.random.randint(50000, 200000, nb_projets)

# Création du DataFrame
data = pd.DataFrame({
    'Taille_du_projet': tailles_projet,
    'Complexite': complexites,
    'Nombre_de_ressources_humaines': nb_ressources_humaines,
    'Nombre_de_ressources_materielles': nb_ressources_materielles,
    'Duree_du_projet': durees_projet,
    'Risques_potentiels': risques,
    'Cout_du_projet': couts_projet

})

# Affichage des premières lignes du DataFrame
print(data.head())

# Enregistrement du jeu de données dans un fichier CSV
data.to_csv('data.csv', index=False)
