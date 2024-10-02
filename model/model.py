# Importation des bibliothèques nécessaires
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

# Chargement des données depuis un fichier Excel (xlsx)
data = pd.read_excel("data.xlsx")

# Séparation des variables explicatives (X) et de la variable cible (y)
X = data[['Taille_projet', 'Duree_estimee']]
y = data['Couts_reels']

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraînement du modèle de régression linéaire
model_linear = LinearRegression()
model_linear.fit(X_train, y_train)
y_pred_linear = model_linear.predict(X_test)
mse_linear = mean_squared_error(y_test, y_pred_linear)

# Entraînement du modèle de forêts aléatoires
model_rf = RandomForestRegressor(random_state=42)
model_rf.fit(X_train, y_train)
y_pred_rf = model_rf.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)

# Entraînement du modèle de réseau de neurones
model_nn = MLPRegressor(random_state=42)
model_nn.fit(X_train, y_train)
y_pred_nn = model_nn.predict(X_test)
mse_nn = mean_squared_error(y_test, y_pred_nn)

# Affichage des résultats
print("Erreur quadratique moyenne (Régression linéaire) :", mse_linear)
print("Erreur quadratique moyenne (Forêts aléatoires) :", mse_rf)
print("Erreur quadratique moyenne (Réseau de neurones) :", mse_nn)
