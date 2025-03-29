# ----- Import des librairies -----

from app import create_app

# Créer l'application Flask
app = create_app()

# Lancer l'application
if __name__ == "__main__":
    app.run(debug=True)