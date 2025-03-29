# ----- Import des librairies -----

import mysql.connector

# Connexion à la BDD
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='amandine',
        database='dossier_medical'
    )