# ----- Import des librairies -----

import numpy as np
from PIL import Image
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras import layers

# ----- Pre processing -----

# Charger une image par
def load_image(image_path):
    try:
        return Image.open(image_path)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image {image_path}: {e}")
        return None

# Charger toutes les images d'un dossier
def load_images(base_path):
    images = []
    for fichier in os.listdir(base_path):
        image_path = os.path.join(base_path, fichier)
        img = load_image(image_path)
        if img is not None:
            images.append(img)
    return images

        
# Charger toutes les images où les patients sont atteint de SEP 
sep_images = load_images('app/data/sep')
# Charger toutes les images où les patients ne sont pas atteint de SEP 
nosep_images = load_images('app/data/nosep')

# Nombre d'observations dans chacune des classes
print(f"Nombre d'images SEP chargées : {len(sep_images)}")
print(f"Nombre d'images sans SEP chargées : {len(nosep_images)}")

# Redimensionner et normaliser une image
def preprocess_image(img, target_size=(224, 224)):
    img_resized = img.resize(target_size)
    img_resized = img_resized.convert('RGB')
    # Normalisation entre 0 et 1
    img_array = np.array(img_resized) / 255.0  
    return img_array

# Pré-traitement des images
normalized_sep_images = []

for img in sep_images:
    normalized_sep_images.append(preprocess_image(img))

normalized_nosep_images = []

for img in nosep_images:
    normalized_nosep_images.append(preprocess_image(img))

# Création des labels
# 0 = pas de SEP
# 1 = SEP
sep_labels = np.ones(len(normalized_sep_images))
nosep_labels = np.zeros(len(normalized_nosep_images))

# Concaténer les données et les labels
all_images = np.concatenate([normalized_sep_images, normalized_nosep_images], axis=0)
all_labels = np.concatenate([sep_labels, nosep_labels], axis=0)

# ----- Machine Learning -----

# Diviser le jeu de données en trois sous ensembles 
# Un ensemble d'entraînement, un ensemble de validation et un ensemble de test
# 70% de données d'entraînement, 15% de données de validation et 15% de données de test
X_train, X_temp, y_train, y_temp = train_test_split(all_images, all_labels, test_size=0.3, random_state=42, stratify=all_labels)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5,)

# Construction du modèle 
# Modèle CNN très simple dû au manque de données
model = tf.keras.Sequential([
    layers.Input(shape=(224, 224, 3)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.build()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Stoppe l'entraînement si la validation ne s'améliore plus après 10 epochs
early_stopping = EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)
# Réduit le learning rate si la validation stagne
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)

# Entrainer le modèle
history = model.fit(X_train, y_train, epochs=20, batch_size=3, validation_data=(X_val, y_val), callbacks=[early_stopping, reduce_lr])

# Evaluation du modèle sur les données de test
test_loss, test_accuracy = model.evaluate(X_test, y_test)

print(f"Test Loss: {test_loss:.2f}")
print(f"Test Accuracy: {test_accuracy:.2%}")

# Sauvegarder le modèle
model.save('app/models/sep_detection_model.keras')