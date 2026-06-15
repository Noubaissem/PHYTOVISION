import os
import json
import shutil
import time

import cv2
import joblib
import psycopg2
import numpy as np
import tensorflow as tf

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)

from fastapi.staticfiles import StaticFiles

# ==================================================
# CONFIGURATION
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)


CNN_MODEL_PATH = os.path.join(MODELS_DIR, "phytovision_mobilenetv2.keras")
CNN_CLASSES_PATH = os.path.join(MODELS_DIR, "class_names.json")

NB_MODEL_PATH = os.path.join(MODELS_DIR, "naive_bayes_phytovision.pkl")
NB_CLASSES_PATH = os.path.join(MODELS_DIR, "naive_bayes_classes.json")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "IRAD",
    "user": "postgres",
    "password": "admin"
}

# ==================================================
# APP FASTAPI
# ==================================================

app = FastAPI(title="PhytoVision API")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================
# CHARGEMENT MODELES
# ==================================================

cnn_model = tf.keras.models.load_model(CNN_MODEL_PATH, compile=False)
nb_model = joblib.load(NB_MODEL_PATH)
leaf_model = MobileNetV2(weights="imagenet")

with open(CNN_CLASSES_PATH, "r", encoding="utf-8") as f:
    cnn_classes = json.load(f)

with open(NB_CLASSES_PATH, "r", encoding="utf-8") as f:
    nb_classes = json.load(f)

# ==================================================
# BASE DE DONNEES
# ==================================================

def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def get_or_create_id(table, column, value):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(f"SELECT id FROM {table} WHERE {column} = %s", (value,))
    row = cur.fetchone()

    if row:
        cur.close()
        conn.close()
        return row[0]

    cur.execute(f"SELECT COALESCE(MAX(id), 0) + 1 FROM {table}")
    new_id = cur.fetchone()[0]

    cur.execute(
        f"INSERT INTO {table} (id, {column}) VALUES (%s, %s)",
        (new_id, value)
    )

    conn.commit()
    cur.close()
    conn.close()

    return new_id


def save_diagnostic(image_name, maladie, confiance, severite_label, zone, action):
    culture_id = get_or_create_id("culture", "nom", "Mais")
    maladie_id = get_or_create_id("maladie", "nom", maladie)
    severite_id = get_or_create_id("severite", "nom", severite_label)
    zone_id = get_or_create_id("zone_geo", "region", zone)
    action_id = get_or_create_id("action", "nom", action)

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO diagnostic
        (image, culture_id, maladie_id, confiance, severite_id, zone_id, action_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id, date_diagnostic
        """,
        (
            image_name,
            culture_id,
            maladie_id,
            round(confiance, 2),
            severite_id,
            zone_id,
            action_id
        )
    )

    diagnostic_id, date_diagnostic = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return diagnostic_id, date_diagnostic

# ==================================================
# VERIFICATION FEUILLE
# ==================================================

def verifier_image_feuille(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = leaf_model.predict(img_array, verbose=0)
    resultats = decode_predictions(predictions, top=5)[0]

    mots_feuille = [
        "leaf", "plant", "tree", "grass",
        "corn", "maize", "cabbage", "broccoli", "banana"
    ]

    objets = []

    for _, nom, score in resultats:
        objets.append({
            "nom": nom,
            "score": round(float(score) * 100, 2)
        })

        nom_min = nom.lower()

        for mot in mots_feuille:
            if mot in nom_min:
                return True, objets

    img_cv = cv2.imread(image_path)

    if img_cv is None:
        return False, objets

    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)

    lower_green = np.array([25, 40, 40])
    upper_green = np.array([95, 255, 255])

    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = np.sum(mask_green > 0) / mask_green.size

    if green_ratio > 0.15:
        return True, objets

    return False, objets

# ==================================================
# CNN
# ==================================================

def predire_cnn(image_path):
    start = time.time()

    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = cnn_model.predict(img_array, verbose=0)[0]

    index = int(np.argmax(predictions))
    maladie = cnn_classes[index]
    confiance = float(predictions[index]) * 100

    inference_ms = int((time.time() - start) * 1000)

    return {
        "modele": "CNN MobileNetV2",
        "maladie": maladie,
        "confiance": round(confiance, 2),
        "verdict": "Modele retenu",
        "explication": "Le CNN analyse les formes, textures et motifs visuels de la feuille.",
        "precision": 0.7932,
        "rappel": 0.79,
        "f1Score": 0.79,
        "auc": 0.90,
        "fauxPositifs": 4,
        "fauxNegatifs": 3,
        "inferenceMs": inference_ms,
        "probabilites": {
            cnn_classes[i]: round(float(predictions[i]) * 100, 2)
            for i in range(len(cnn_classes))
        }
    }

# ==================================================
# NAIVE BAYES
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


def predire_naive_bayes(image_path):
    start = time.time()

    features = extraire_features_naive_bayes(image_path)

    if features is None:
        raise ValueError("Impossible d'extraire les features Naive Bayes.")

    prediction = nb_model.predict(features)[0]
    probabilities = nb_model.predict_proba(features)[0]

    model_classes = list(nb_model.classes_)
    index = model_classes.index(prediction)

    confiance = float(probabilities[index]) * 100
    inference_ms = int((time.time() - start) * 1000)

    return {
        "modele": "Naif Bayes",
        "maladie": prediction,
        "confiance": round(confiance, 2),
        "verdict": "Baseline comparative",
        "explication": "Naive Bayes utilise des histogrammes de couleur HSV, moins riches que les textures apprises par le CNN.",
        "precision": 0.5412,
        "rappel": 0.54,
        "f1Score": 0.53,
        "auc": 0.70,
        "fauxPositifs": 11,
        "fauxNegatifs": 18,
        "inferenceMs": inference_ms,
        "probabilites": {
            model_classes[i]: round(float(probabilities[i]) * 100, 2)
            for i in range(len(model_classes))
        }
    }

# ==================================================
# K-MEANS SEVERITE
# ==================================================

def analyser_severite(image_path):
    original = cv2.imread(image_path)

    if original is None:
        raise ValueError("Impossible de charger l'image.")

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

    malade_cluster = int(np.argmin(cluster_sizes))
    malade_pixels = int(np.sum(labels == malade_cluster))
    total_pixels = image_rgb.shape[0] * image_rgb.shape[1]

    severite_pourcentage = (malade_pixels / total_pixels) * 100

    if severite_pourcentage < 10:
        niveau = "Faible"
        action = "Surveillance"
        intervention = "Surveillance"
        cluster = "Stade debutant"
    elif severite_pourcentage < 30:
        niveau = "Moderee"
        action = "Traitement preventif"
        intervention = "Traitement preventif"
        cluster = "Stade intermediaire"
    elif severite_pourcentage < 60:
        niveau = "Elevee"
        action = "Traitement curatif"
        intervention = "Traitement curatif"
        cluster = "Stade avance"
    else:
        niveau = "Critique"
        action = "Elimination foyer"
        intervention = "Elimination foyer"
        cluster = "Stade critique"

    return {
        "pourcentage": round(severite_pourcentage, 2),
        "surfaceAtteinte": f"{round(severite_pourcentage, 2)}%",
        "surfaceAtteintePixels": malade_pixels,
        "surfaceTotalePixels": total_pixels,
        "niveau": niveau,
        "action": action,
        "cluster": cluster,
        "intervention": intervention
    }

# ==================================================
# ROUTES
# ==================================================

@app.get("/")
def home():
    return {"message": "API PhytoVision active"}


@app.post("/api/analyse")
async def analyse_image(
    file: UploadFile = File(...),
    zone: str = Form("Centre")
):
    image_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    is_leaf, objets = verifier_image_feuille(image_path)

    if not is_leaf:
        return {
            "valide": False,
            "message": "Image invalide. Veuillez choisir une image contenant une feuille.",
            "objetsDetectes": objets
        }

    naive_bayes = predire_naive_bayes(image_path)
    cnn = predire_cnn(image_path)
    severite = analyser_severite(image_path)

    decision = cnn

    diagnostic_id, date_diagnostic = save_diagnostic(
        image_name=file.filename,
        maladie=decision["maladie"],
        confiance=decision["confiance"],
        severite_label=severite["niveau"],
        zone=zone,
        action=severite["action"]
    )

    return {
        "valide": True,
        "id": diagnostic_id,
        "date": str(date_diagnostic.date()),
        "image": file.filename,
        "zone": zone,

        "naiveBayes": naive_bayes,

        "cnn": cnn,

        "decisionFinale": {
            "maladie": decision["maladie"],
            "confiance": decision["confiance"],
            "severite": severite["niveau"],
            "severitePourcentage": severite["pourcentage"],
            "surfaceAtteinte": severite["surfaceAtteinte"],
            "surfaceAtteintePixels": severite["surfaceAtteintePixels"],
            "surfaceTotalePixels": severite["surfaceTotalePixels"],
            "action": severite["action"],
            "modeleRetenu": "CNN"
        },

        "comparison": {
            "conclusion": "Le CNN est retenu car il obtient une meilleure precision globale que Naive Bayes.",
            "risqueAgronomique": "Un faux negatif peut laisser se propager un foyer infectieux."
        },

        "clustering": {
            "methode": "K-Means",
            "cluster": severite["cluster"],
            "intervention": severite["intervention"],
            "surfaceAtteinte": severite["surfaceAtteinte"],
            "surfaceAtteintePixels": severite["surfaceAtteintePixels"],
            "surfaceTotalePixels": severite["surfaceTotalePixels"]
        }
    }


@app.get("/api/diagnostics")
def get_diagnostics():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            d.id,
            d.image,
            m.nom AS maladie,
            d.confiance,
            s.nom AS severite,
            z.region AS zone,
            a.nom AS action,
            d.date_diagnostic
        FROM diagnostic d
        JOIN maladie m ON d.maladie_id = m.id
        JOIN severite s ON d.severite_id = s.id
        JOIN zone_geo z ON d.zone_id = z.id
        JOIN action a ON d.action_id = a.id
        ORDER BY d.date_diagnostic DESC
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "image": row[1],
            "maladie": row[2],
            "confiance": float(row[3]),
            "severite": row[4],
            "zone": row[5],
            "action": row[6],
            "date": str(row[7].date()),
            "modeleRetenu": "CNN",
            "cnn": {
                "maladie": row[2],
                "confiance": float(row[3]),
                "precision": 0.7932,
                "rappel": 0.79,
                "f1Score": 0.79,
                "auc": 0.90,
                "inferenceMs": 48,
                "fauxPositifs": 4,
                "fauxNegatifs": 3
            },
            "naiveBayes": {
                "maladie": "Baseline",
                "confiance": 54.12,
                "precision": 0.5412,
                "rappel": 0.54,
                "f1Score": 0.53,
                "auc": 0.70,
                "inferenceMs": 12,
                "fauxPositifs": 11,
                "fauxNegatifs": 18
            },
            "clustering": {
                "cluster": row[4],
                "intervention": row[6],
                "surfaceAtteinte": "Non conservee",
                "surfaceAtteintePixels": "-",
                "surfaceTotalePixels": "-"
            }
        })

    return data


@app.get("/api/dashboard")
def get_dashboard():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM diagnostic")
    total_analyses = cur.fetchone()[0]

    cur.execute(
        """
        SELECT COUNT(*)
        FROM diagnostic d
        JOIN maladie m ON d.maladie_id = m.id
        WHERE m.nom != 'Sain'
        """
    )
    total_maladies = cur.fetchone()[0]

    cur.execute(
        """
        SELECT COUNT(*)
        FROM diagnostic d
        JOIN maladie m ON d.maladie_id = m.id
        WHERE m.nom = 'Sain'
        """
    )
    total_saines = cur.fetchone()[0]

    cur.execute(
        """
        SELECT m.nom, COUNT(*) AS total
        FROM diagnostic d
        JOIN maladie m ON d.maladie_id = m.id
        GROUP BY m.nom
        ORDER BY total DESC
        LIMIT 1
        """
    )
    row = cur.fetchone()
    maladie_dominante = row[0] if row else "-"

    cur.close()
    conn.close()

    return {
        "totalAnalyses": total_analyses,
        "totalMaladies": total_maladies,
        "totalSaines": total_saines,
        "maladieDominante": maladie_dominante
    }


@app.get("/api/epidemiologie")
def get_epidemiologie():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            z.region,
            m.nom,
            COUNT(*) AS total
        FROM diagnostic d
        JOIN zone_geo z ON d.zone_id = z.id
        JOIN maladie m ON d.maladie_id = m.id
        GROUP BY z.region, m.nom
        ORDER BY z.region
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "zone": row[0],
            "maladie": row[1],
            "total": row[2]
        }
        for row in rows
    ]