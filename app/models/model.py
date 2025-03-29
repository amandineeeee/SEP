# ----- Import des librairies -----

from tensorflow.keras.models import load_model
import numpy as np 
from PIL import Image
import keras
# Import de la classe Config définie dans le fichier config.py
from config import Config


# ----- Prédictions -----

# Charger le modèle pré-entraîné
def load_trained_model():
    keras.config.enable_unsafe_deserialization()
    return load_model(Config.MODEL_PATH)

# ----- Pré-traitement de l'image -----

# Le but est qu'elle ait la taille et le format attendu par le modèle
def preprocess_image(img):
    img = img.resize((224, 224))  
    img_array = np.array(img)
    img_array = img_array / 255.0  
    img_array = np.expand_dims(img_array, axis=0) 
    return img_array

# Renvoie la prédiction pour une image donnée
def predict_image(image_path):
    model = load_trained_model()
    img = Image.open(image_path).convert('RGB')
    img_array = preprocess_image(img)

    prediction = model.predict(img_array)
    return "SEP détectée" if prediction[0][0] > 0.5 else "Pas de SEP détectée"