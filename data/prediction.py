import pandas as pd
import pickle

# Charger le modèle à partir du fichier .pkl
model_path = 'model.pkl'
model = pickle.load(open(model_path, 'rb'))

def predict_cost(taille_projet, complexite, nb_ressources_humaines, nb_ressources_materielles, duree_projet, risques):
    # Assurez-vous que la complexité et les risques sont bien formatés
    complexite = complexite.capitalize()
    risques = risques.capitalize()

    # Convertir les caractéristiques en DataFrame
    features = {
        'Taille_du_projet': [taille_projet],
        'Complexite': [complexite],
        'Nombre_de_ressources_humaines': [nb_ressources_humaines],
        'Nombre_de_ressources_materielles': [nb_ressources_materielles],
        'Duree_du_projet': [duree_projet],
        'Risques_potentiels': [risques]
    }
    features_df = pd.DataFrame(features)

    # Faire une prédiction
    predicted_cost = model.predict(features_df)
    return predicted_cost[0]
