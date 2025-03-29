# ----- Import des librairies -----

import os

class Config:
    # Clé secrète afin de sécuriser les sessions
    SECRET_KEY = os.urandom(24)
    # Chemin vers le modèle de Machine Learning
    MODEL_PATH = "app/models/sep_detection_model.keras"
    # Extensions autorisées
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}