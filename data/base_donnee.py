from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ma_base_de_donnees.db'
db = SQLAlchemy(app)

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    telephone = db.Column(db.String(20), nullable=True)  # Ajout du champ numéro de téléphone
    role = db.Column(db.String(10), nullable=False)

class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    
    projet_pdf = db.Column(db.String(255))  # Champ pour stocker le chemin du fichier PDF

class Predict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taille_projet = db.Column(db.Integer)
    complexite_projet = db.Column(db.String(255))
    nb_ressources_humaines = db.Column(db.Integer)
    nb_ressources_materielles = db.Column(db.Integer)
    duree_projet_months = db.Column(db.Integer)
    risques_potentiels = db.Column(db.String(1000))
    cout_predit = db.Column(db.Float)


with app.app_context():
    db.create_all()

