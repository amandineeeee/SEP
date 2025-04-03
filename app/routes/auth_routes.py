# ----- Import des librairies -----

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
# Import de la fonction contenue dans le fichie db.py 
# Cette fonction permet de se connecter à la BDD
from app.db import get_db_connection

# Création du Blueprint auth
# Il permet d'organiser les routes liées à l'authentification
auth_bp = Blueprint('auth', __name__)

# ----- Définition des routes -----

# Route pour la page d'accueil
@auth_bp.route('/')
def home():
    # Si l'utilisateur est déjà connecté 
    if 'username' in session:
        # Le rediriger vers la pages du dashboard des patients
        return redirect(url_for('patient.get_patients'))
    # Sinon le rediriger vers la page de connexion
    return render_template('index.html')

# Route pour gérer la connexion
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Vérifier que la requête soit de type POST
    if request.method == 'POST':
        # Récupérer les données envoyées par le formulaire
        username = request.form['username']
        password = request.form['password']
        
        # Vérifier si le nom d'utilisateur existe dans la base de données
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Utilisateur WHERE username = %s", (username,))
        user = cursor.fetchone()

        # Si l'utilisateur existe
        if user:
            # Vérifier le mot de passe hashé
            if check_password_hash(user['password'], password):  
                # Ajouter le nom d'utilisateur et le role à la session
                session['username'] = username  
                session['role'] = user['role'] 
                # Rediriger vers la page d'accueil
                return redirect(url_for('auth.home'))
            # Sinon rediriger vers la page de connexion  
            else:
                return render_template('index.html', error="Mot de passe incorrect")
        # Si l'utilisateur n'existe pas rediriger vers la page de connexion
        else:
            return render_template('index.html', error="Nom d'utilisateur incorrect")
    return render_template('index.html')

# Route pour gérer la déconnexion
@auth_bp.route('/logout')
def logout():
    # Supprime username et role de la session
    session.pop('username', None)  
    session.pop('role', None)  
    # Redirige l'utilisateur vers la page de connexion
    return redirect(url_for('auth.login'))  

@auth_bp.route('/creerCompte')
def createAccount():
    return render_template('creer_compte.html')

@auth_bp.route('/enregistrer_compte',  methods=['POST'])
def registerAccount():
    # Vérifier que la requête soit de type POST
    if request.method == 'POST':
        # Récupérer les données envoyées par le formulaire
        username = request.form['username']
        password = request.form['password']
        statut = request.form['statut']
        # Hacher le mot de passe
        hashed_password = generate_password_hash(password)

        # Connexion à la BDD
        conn = get_db_connection()
        cursor = conn.cursor()

         # Vérifier si le username existe déjà
        cursor.execute("SELECT * FROM Utilisateur WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.", "danger")
            return redirect(url_for('auth.createAccount'))
        
        cursor.execute("""
            INSERT INTO Utilisateur (username, password, role)
            VALUES (%s, %s, %s)
        """, (username, hashed_password, statut))
        conn.commit()
        conn.close()

    return render_template('index.html')