# ----- Import des librairies -----

from flask import Flask
# Import des blueprints
from .routes.auth_routes import auth_bp
from .routes.patient_routes import patient_bp

def create_app():
    # Créer une instance de l'application Flask
    app = Flask(__name__, static_folder='static', template_folder='templates')
    # Charger la configuration
    app.config.from_object('config.Config')
    # Enregistrer les blueprints dans l'application
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)

    return app
