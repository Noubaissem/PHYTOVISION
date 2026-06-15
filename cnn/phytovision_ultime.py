import os
import json
import cv2
import joblib
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

MODE_PREDICTION = "NAIVE_BAYES"
# MODE_PREDICTION = "NAIVE_BAYES"
# MODE_PREDICTION = "CNN"

IMAGE_PATH = r"C:\Users\PC\Documents\Projet IA\Maize\Sain\AUG_91be18ce.jpg"

CNN_MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "phytovision_mobilenetv2.keras"
)

CNN_CLASSES_PATH = os.path.join(
    BASE_DIR,
    "models",
    "class_names.json"
)

NB_MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "naive_bayes_phytovision.pkl"
)

NB_CLASSES_PATH = os.path.join(
    BASE_DIR,
    "models",
    "naive_bayes_classes.json"
)

# ==================================================
# VERIFICATION FEUILLE
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
# FEATURES NAIVE BAYES
# ==================================================

def extraire_features_naive_bayes(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None

    img = cv2.resize(img, (128, 128))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hist_h = cv2.calcHist([hsv], [0], None, [32], [0, 180])
    hist_s = cv2.calcHist([hsv], [1], None, [32], [0, 256])
    hist_v = cv2.calcHist([hsv], [2], None, [32], [0, 256])

    features = np.concatenate([
        hist_h.flatten(),
        hist_s.flatten(),
        hist_v.flatten()
    ])

    features = features / np.sum(features)

    return features.reshape(1, -1)

# ==================================================
# PREDICTION CNN
# ==================================================

def predire_cnn(image_path):
    with open(CNN_CLASSES_PATH, "r", encoding="utf-8") as f:
        classes = json.load(f)

    model = tf.keras.models.load_model(
        CNN_MODEL_PATH,
        compile=False
    )

    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array, verbose=0)[0]

    index = int(np.argmax(predictions))
    maladie = classes[index]
    confiance = float(predictions[index]) * 100

    return maladie, confiance, predictions, classes

# ==================================================
# PREDICTION NAIVE BAYES
# ==================================================

def predire_naive_bayes(image_path):
    with open(NB_CLASSES_PATH, "r", encoding="utf-8") as f:
        classes = json.load(f)

    model = joblib.load(NB_MODEL_PATH)

    features = extraire_features_naive_bayes(image_path)

    if features is None:
        raise ValueError("Impossible d'extraire les caracteristiques de l'image.")

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    model_classes = list(model.classes_)

    index = model_classes.index(prediction)

    confiance = float(probabilities[index]) * 100

    # Réordonner les probabilités selon l'ordre du fichier classes
    probs_reordonnees = []

    for classe in classes:
        if classe in model_classes:
            i = model_classes.index(classe)
            probs_reordonnees.append(probabilities[i])
        else:
            probs_reordonnees.append(0.0)

    return prediction, confiance, np.array(probs_reordonnees), classes

# ==================================================
# ANALYSE DE SEVERITE K-MEANS
# ==================================================

def analyser_severite(image_path):
    original = cv2.imread(image_path)

    if original is None:
        raise ValueError("Impossible de charger l'image avec OpenCV.")

    image_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

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

    cluster_sizes = []

    for i in range(K):
        cluster_sizes.append(np.sum(labels == i))

    malade_cluster = np.argmin(cluster_sizes)
    malade_pixels = np.sum(labels == malade_cluster)

    total_pixels = image_rgb.shape[0] * image_rgb.shape[1]

    severite = (malade_pixels / total_pixels) * 100

    if severite < 10:
        niveau = "Faible"
    elif severite < 30:
        niveau = "Moderee"
    elif severite < 60:
        niveau = "Elevee"
    else:
        niveau = "Critique"

    return severite, niveau

# ==================================================
# PROGRAMME PRINCIPAL
# ==================================================

if not verifier_image_feuille(IMAGE_PATH):
    print("\n===================================")
    print("        PHYTOVISION REPORT")
    print("===================================")
    print("\nImage invalide.")
    print("Veuillez choisir une image contenant une feuille.")
    print("\n===================================")
    exit()

if MODE_PREDICTION.upper() == "CNN":
    maladie, confiance, probabilities, classes = predire_cnn(IMAGE_PATH)
    modele_utilise = "CNN MobileNetV2"

elif MODE_PREDICTION.upper() == "NAIVE_BAYES":
    maladie, confiance, probabilities, classes = predire_naive_bayes(IMAGE_PATH)
    modele_utilise = "Naive Bayes"

else:
    print("Erreur : MODE_PREDICTION doit etre 'CNN' ou 'NAIVE_BAYES'.")
    exit()

severite, niveau = analyser_severite(IMAGE_PATH)

recommandations = {
    "Sain": "Aucune action necessaire.",
    "Virus_de_la_strie": "Surveiller la propagation et eliminer les feuilles tres atteintes.",
    "Brulure_foliaire": "Traitement fongicide recommande.",
    "Tache_grise": "Controle phytosanitaire recommande."
}

print("\n")
print("===================================")
print("        PHYTOVISION ULTIME")
print("===================================")

print("\nImage :")
print(os.path.basename(IMAGE_PATH))

print("\nModele utilise :")
print(modele_utilise)

print("\nMaladie detectee :")
print(maladie)

print("\nConfiance :")
print(f"{confiance:.2f}%")

print("\nSeverite :")
print(f"{severite:.2f}%")

print("\nNiveau :")
print(niveau)

print("\nRecommandation :")
print(recommandations.get(maladie, "Aucune recommandation disponible."))

print("\nProbabilites :")
for nom, score in zip(classes, probabilities):
    print(f"{nom} : {score * 100:.2f}%")

print("\n===================================")