from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import request
from flask import request, jsonify
from base_donnee import Predict
from prediction import predict_cost
from base_donnee import Utilisateur
from flask import Flask, render_template, send_file
from flask import send_file
from flask import abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ma_base_de_donnees.db'
app.config['SECRET_KEY'] = 'votre_secret_key_ici'
db = SQLAlchemy(app)
UPLOAD_FOLDER = '/home/kali/Desktop/Fadwa/data/projet'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

class predict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taille_projet = db.Column(db.Integer)
    complexite_projet = db.Column(db.String(255))
    nb_ressources_humaines = db.Column(db.Integer)
    nb_ressources_materielles = db.Column(db.Integer)
    duree_projet_months = db.Column(db.Integer)
    risques_potentiels = db.Column(db.String(1000))
    cout_predit = db.Column(db.Float)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and request.form['action'] == 'connexion':
        username = request.form['username']
        password = request.form['password']
        
        user = Utilisateur.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for(f'{user.role}_dashboard'))
        else:
            return render_template('index.html', message='Nom d’utilisateur ou mot de passe incorrect')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        adresse = request.form['adresse']
        telephone = request.form['telephone']
        role = request.form['role']
        
        existing_user = Utilisateur.query.filter_by(username=username).first()
        if existing_user:
            return 'Cet utilisateur existe déjà!'
        
        new_user = Utilisateur(nom=nom, prenom=prenom, username=username, password=password, email=email, adresse=adresse, telephone=telephone, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    # Votre logique de déconnexion ici
    session.clear()  # Effacer la session de l'utilisateur
    return redirect(url_for('index'))
    
    
@app.route('/import_project', methods=['POST'])
def import_project():
    if request.method == 'POST':
        titre = request.form['project_title']
        description = request.form['project_description']
        pdf_file = request.files['project_pdf']  # Obtenez le fichier PDF téléchargé

        # Vérifiez si un fichier a été téléchargé
        if pdf_file:
            # Enregistrez le fichier PDF téléchargé dans un répertoire de votre choix
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)
        else:
            # Gérez l'absence de fichier PDF téléchargé
            pass  # Remplacez cela par le code approprié si nécessaire

        # Obtenez l'ID de l'utilisateur actuellement connecté à partir de la session
        # utilisateur_id = session['user_id']
        # Pour cet exemple, j'utilise une valeur arbitraire 1 pour l'utilisateur_id
        utilisateur_id = 1
        
        new_project = Projet(titre=titre, description=description, utilisateur_id=utilisateur_id, projet_pdf=pdf_path)
        db.session.add(new_project)
        db.session.commit()
        
        return redirect(url_for('client_dashboard'))

    return redirect(url_for('client_dashboard'))


@app.route('/back_to_client_dashboard')
def back_to_client_dashboard():
    # Rediriger vers l'interface client
    return redirect(url_for('client_dashboard'))    

@app.route('/liste_clients')
def liste_clients():
    # Récupération des noms et prénoms des clients depuis la base de données
    clients = Utilisateur.query.filter_by(role='client').with_entities(Utilisateur.nom, Utilisateur.prenom, Utilisateur.telephone, Utilisateur.email).all()

    # Rendu de la page HTML avec la liste des clients
    return render_template('liste_clients.html', clients=clients)


# Route pour télécharger le fichier PDF
@app.route('/download_pdf/<int:projet_id>')
def download_pdf(projet_id):
    # Ici, vous devrez ajouter la logique pour récupérer le fichier PDF en fonction de l'identifiant du projet
    # Supposons que vous ayez un fichier PDF nommé 'projet_<projet_id>.pdf' dans un dossier 'pdf'
    # Assurez-vous d'adapter ce code en fonction de votre logique de récupération des fichiers PDF
    filename = f'pdf/projet_{projet_id}.pdf'
    return send_file(filename, as_attachment=True)


def download_pdf(projet_id):
    # Construire le chemin d'accès complet au fichier PDF en utilisant l'identifiant du projet
    filename = f'/home/kali/Desktop/Fadwa/data/projet/projet_{projet_id}.pdf'
    
    try:
        # Renvoyer le fichier PDF en tant que téléchargement
        return send_file(filename, as_attachment=True)
    except FileNotFoundError:
        # Gérer l'erreur si le fichier PDF n'est pas trouvé
        return "Fichier PDF introuvable"


        
@app.route('/client')
def client_dashboard():
    if 'role' in session and session['role'] == 'client':
        return render_template('client.html')
    else:
        return redirect(url_for('index'))

@app.route('/owner')
def owner_dashboard():
    if 'role' in session and session['role'] == 'owner':
        return render_template('owner.html')
    else:
        return redirect(url_for('index'))

@app.route('/liste_projets')
def liste_projets():
    projets = Projet.query.all()
    return render_template('liste_projets.html', projets=projets)

@app.route('/predict', methods=['POST'])
def make_prediction():
    data = request.get_json()
    taille_projet = int(data['taille_projet'])
    complexite = data['complexite']
    nb_ressources_humaines = int(data['nb_ressources_humaines'])
    nb_ressources_materielles = int(data['nb_ressources_materielles'])
    duree_projet = int(data['duree_projet'])
    risques = data['risques']

    # Effectuer la prédiction du coût
    prediction = predict_cost(taille_projet, complexite, nb_ressources_humaines, nb_ressources_materielles, duree_projet, risques)

    # Enregistrer les informations de prédiction dans la base de données
    new_prediction = Predict(
        taille_projet=taille_projet,
        complexite_projet=complexite,
        nb_ressources_humaines=nb_ressources_humaines,
        nb_ressources_materielles=nb_ressources_materielles,
        duree_projet_months=duree_projet,
        risques_potentiels=risques,
        cout_predit=prediction
    )
    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({'prediction': prediction})
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
