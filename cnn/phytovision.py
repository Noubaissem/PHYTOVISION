import os
import json
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)

# ==================================================
# CONFIGURATION
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "phytovision_mobilenetv2.keras"
)

CLASS_NAMES_PATH = os.path.join(
    BASE_DIR,
    "models",
    "class_names.json"
)

IMAGE_PATH = r"C:\Users\PC\Documents\Projet IA\Maize\Sain\AUG_91be18ce.jpg"

# ==================================================
# VERIFICATION : IMAGE FEUILLE OU NON
# ==================================================

def verifier_image_feuille(image_path):
    print("\nVerification de l'image...")

    verifier_model = MobileNetV2(weights="imagenet")

    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = verifier_model.predict(img_array, verbose=0)
    resultats = decode_predictions(predictions, top=5)[0]

    mots_feuille = [
        "leaf",
        "plant",
        "tree",
        "grass",
        "corn",
        "maize",
        "cabbage",
        "broccoli",
        "banana"
    ]

    print("\nObjets reconnus :")
    for _, nom, score in resultats:
        print(f"- {nom} : {score * 100:.2f}%")

        nom_min = nom.lower()

        for mot in mots_feuille:
            if mot in nom_min:
                print("\nImage acceptee : feuille ou plante detectee.")
                return True

    # Verification complementaire : presence de vert
    img_cv = cv2.imread(image_path)

    if img_cv is None:
        print("\nImage refusee : fichier image illisible.")
        return False

    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)

    lower_green = np.array([25, 40, 40])
    upper_green = np.array([95, 255, 255])

    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    green_ratio = np.sum(mask_green > 0) / mask_green.size

    print(f"\nTaux de vegetation detecte : {green_ratio * 100:.2f}%")

    if green_ratio > 0.15:
        print("\nImage acceptee : forte presence de vegetation.")
        return True

    print("\nImage refusee : aucune feuille detectee.")
    return False


# ==================================================
# CONTROLE AVANT ANALYSE
# ==================================================

if not verifier_image_feuille(IMAGE_PATH):
    print("\n===================================")
    print("        PHYTOVISION REPORT")
    print("===================================")
    print("\nImage invalide.")
    print("Veuillez choisir une image contenant une feuille.")
    print("\n===================================")
    exit()

# ==================================================
# CHARGEMENT DES CLASSES
# ==================================================

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    classes = json.load(f)

# ==================================================
# CHARGEMENT DU MODELE CNN MALADIE
# ==================================================

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

# ==================================================
# PREDICTION CNN MALADIE
# ==================================================

img = image.load_img(
    IMAGE_PATH,
    target_size=(224, 224)
)

img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

predictions = model.predict(
    img_array,
    verbose=0
)[0]

index = int(np.argmax(predictions))

maladie = classes[index]

confiance = float(predictions[index]) * 100

# ==================================================
# ANALYSE DE SEVERITE (K-MEANS)
# ==================================================

original = cv2.imread(IMAGE_PATH)

if original is None:
    print("Erreur : impossible de charger l'image avec OpenCV.")
    exit()

image_rgb = cv2.cvtColor(
    original,
    cv2.COLOR_BGR2RGB
)

pixels = image_rgb.reshape((-1, 3))
pixels = np.float32(pixels)

criteria = (
    cv2.TERM_CRITERIA_EPS +
    cv2.TERM_CRITERIA_MAX_ITER,
    100,
    0.2
)

K = 5

_, labels, centers = cv2.kmeans(
    pixels,
    K,
    None,
    criteria,
    10,
    cv2.KMEANS_RANDOM_CENTERS
)

centers = np.uint8(centers)

cluster_sizes = []

for i in range(K):
    cluster_sizes.append(
        np.sum(labels == i)
    )

malade_cluster = np.argmin(
    cluster_sizes
)

malade_pixels = np.sum(
    labels == malade_cluster
)

total_pixels = (
    image_rgb.shape[0]
    *
    image_rgb.shape[1]
)

severite = (
    malade_pixels /
    total_pixels
) * 100

# ==================================================
# NIVEAU DE RISQUE
# ==================================================

if severite < 10:
    niveau = "Faible"

elif severite < 30:
    niveau = "Moderee"

elif severite < 60:
    niveau = "Elevee"

else:
    niveau = "Critique"

# ==================================================
# RECOMMANDATIONS
# ==================================================

recommandations = {
    "Sain":
        "Aucune action necessaire.",

    "Virus_de_la_strie":
        "Surveiller la propagation et eliminer les feuilles tres atteintes.",

    "Brulure_foliaire":
        "Traitement fongicide recommande.",

    "Tache_grise":
        "Controle phytosanitaire recommande."
}

# ==================================================
# RAPPORT FINAL
# ==================================================

print("\n")
print("===================================")
print("        PHYTOVISION REPORT")
print("===================================")

print("\nImage :")
print(os.path.basename(IMAGE_PATH))

print("\nEtat detectee :")
print(maladie)

print("\nConfiance CNN :")
print(f"{confiance:.2f}%")

print("\nSeverite :")
print(f"{severite:.2f}%")

print("\nNiveau :")
print(niveau)

print("\nRecommandation :")
print(recommandations.get(maladie, "Aucune recommandation disponible."))

print("\n===================================")