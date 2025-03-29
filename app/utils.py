# ----- Import des librairies -----

from datetime import datetime
from flask import session
# Import de la classe Config définie dans le fichier config.py
from config import Config

# Calculer l'age d'un patient à partir de sa date de naissance
def calculer_age(date_naissance):
    today = datetime.today()
    date_naissance = datetime.strptime(date_naissance, "%Y-%m-%d")
    age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))
    return age

# Vérifier si l'utilisateur est connecté
def is_logged_in():
    return 'username' in session

# Vérifier si le fichier en question a un extension autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS