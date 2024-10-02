import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
import pickle

# Charger les données
data = pd.read_csv('data.csv')

# Séparer les caractéristiques et la variable cible
X = data.drop('Cout_du_projet', axis=1)
y = data['Cout_du_projet']

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Prétraitement des données
numeric_features = ['Taille_du_projet', 'Nombre_de_ressources_humaines', 'Nombre_de_ressources_materielles', 'Duree_du_projet']
categorical_features = ['Complexite', 'Risques_potentiels']

numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Modèle de régression linéaire
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Entraîner le modèle
model.fit(X_train, y_train)

# Enregistrer le modèle dans un fichier .pkl
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
