import os
import json
import cv2
import joblib
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ======================
# CHEMINS
# ======================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATASET_DIR = os.path.join(BASE_DIR, "dataset")
IMAGES_DIR = os.path.join(PROJECT_DIR, "Maize")
MODELS_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODELS_DIR, exist_ok=True)

TRAIN_CSV = os.path.join(DATASET_DIR, "train.csv")
VAL_CSV = os.path.join(DATASET_DIR, "val.csv")

MODEL_PATH = os.path.join(MODELS_DIR, "naive_bayes_phytovision.pkl")
CLASS_NAMES_PATH = os.path.join(MODELS_DIR, "naive_bayes_classes.json")

# ======================
# CLASSES
# ======================

label_map = {
    0: "Sain",
    1: "Virus_de_la_strie",
    2: "Brulure_foliaire",
    3: "Tache_grise"
}

class_names = [
    "Sain",
    "Virus_de_la_strie",
    "Brulure_foliaire",
    "Tache_grise"
]

# ======================
# EXTRACTION FEATURES
# ======================

def extraire_features(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return None

    image = cv2.resize(image, (128, 128))

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hist_h = cv2.calcHist([hsv], [0], None, [32], [0, 180])
    hist_s = cv2.calcHist([hsv], [1], None, [32], [0, 256])
    hist_v = cv2.calcHist([hsv], [2], None, [32], [0, 256])

    features = np.concatenate([
        hist_h.flatten(),
        hist_s.flatten(),
        hist_v.flatten()
    ])

    features = features / np.sum(features)

    return features

# ======================
# CHARGEMENT DATASET
# ======================

def charger_dataset(csv_path):
    df = pd.read_csv(csv_path)

    X = []
    y = []

    for _, row in df.iterrows():
        label = label_map[int(row["maladie_id"])]
        image_path = os.path.join(IMAGES_DIR, label, row["image"])

        if not os.path.exists(image_path):
            continue

        features = extraire_features(image_path)

        if features is None:
            continue

        X.append(features)
        y.append(label)

    return np.array(X), np.array(y)

# ======================
# ENTRAINEMENT
# ======================

print("Chargement des donnees train...")
X_train, y_train = charger_dataset(TRAIN_CSV)

print("Chargement des donnees validation...")
X_val, y_val = charger_dataset(VAL_CSV)

print("Images train :", len(X_train))
print("Images validation :", len(X_val))

model = GaussianNB()

print("\nEntrainement Naive Bayes...")
model.fit(X_train, y_train)

# ======================
# EVALUATION
# ======================

y_pred = model.predict(X_val)

accuracy = accuracy_score(y_val, y_pred)

print("\n===== RESULTATS NAIVE BAYES =====")
print(f"Accuracy validation : {accuracy * 100:.2f}%")

print("\nRapport de classification :")
print(classification_report(y_val, y_pred))

print("\nMatrice de confusion :")
print(confusion_matrix(y_val, y_pred, labels=class_names))

# ======================
# SAUVEGARDE
# ======================

joblib.dump(model, MODEL_PATH)

with open(CLASS_NAMES_PATH, "w", encoding="utf-8") as f:
    json.dump(class_names, f, ensure_ascii=False, indent=2)

print("\nModele Naive Bayes sauvegarde ici :")
print(MODEL_PATH)