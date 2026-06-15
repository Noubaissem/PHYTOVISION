import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "phytovision_mobilenetv2.keras")
CLASS_NAMES_PATH = os.path.join(BASE_DIR, "models", "class_names.json")

# Change seulement cette ligne pour tester une autre image
IMAGE_PATH = r"C:\Users\PC\Documents\Projet IA\Maize\Sain\AUG_f1abf1af.jpg"

# ======================
# CHARGEMENT DES CLASSES
# ======================

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    classes = json.load(f)

# ======================
# CHARGEMENT DU MODÈLE
# ======================

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

# ======================
# CHARGEMENT DE L'IMAGE
# ======================

img = image.load_img(IMAGE_PATH, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

# Ne pas faire preprocess_input ici.
# Le modèle contient déjà Rescaling.

# ======================
# PRÉDICTION
# ======================

predictions = model.predict(img_array, verbose=0)[0]

index = int(np.argmax(predictions))
maladie = classes[index]
fiabilite = float(predictions[index]) * 100

print("===== DIAGNOSTIC PHYTOVISION =====")
print("Image analysée :", IMAGE_PATH)
print("Maladie détectée :", maladie)
print(f"Fiabilité du diagnostic : {fiabilite:.2f}%")

print("\nProbabilités :")
for nom, score in zip(classes, predictions):
    print(f"{nom} : {score * 100:.2f}%")