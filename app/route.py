# ----- Import des librairies -----

from flask import Flask, render_template, redirect, url_for, session
# Import des blueprints
from .routes.auth_routes import auth_bp
from .routes.patient_routes import patient_bp

app = Flask(__name__)
app.secret_key = '24072002'

# # Enregistrement des blueprints
# app.register_blueprint(auth_bp)
# app.register_blueprint(patient_bp)

# # Page d'accueil
# @app.route('/')
# def home():
#     if 'username' in session:
#         return redirect(url_for('patient.get_patients'))
#     return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)