import os
import json
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

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

# ======================
# CHARGEMENT CSV
# ======================

train_df = pd.read_csv(TRAIN_CSV)
val_df = pd.read_csv(VAL_CSV)

label_map = {
    0: "Sain",
    1: "Virus_de_la_strie",
    2: "Brulure_foliaire",
    3: "Tache_grise"
}

train_df["label"] = train_df["maladie_id"].map(label_map)
val_df["label"] = val_df["maladie_id"].map(label_map)

train_df["image_path"] = train_df.apply(
    lambda row: os.path.join(IMAGES_DIR, row["label"], row["image"]),
    axis=1
)

val_df["image_path"] = val_df.apply(
    lambda row: os.path.join(IMAGES_DIR, row["label"], row["image"]),
    axis=1
)

train_df = train_df[train_df["image_path"].apply(os.path.exists)]
val_df = val_df[val_df["image_path"].apply(os.path.exists)]

print("Images train :", len(train_df))
print("Images validation :", len(val_df))
print("Classes :", train_df["label"].unique())

# ======================
# DATASET TENSORFLOW
# ======================

IMG_SIZE = (224, 224)
BATCH_SIZE = 16

CLASS_NAMES = [
    "Sain",
    "Virus_de_la_strie",
    "Brulure_foliaire",
    "Tache_grise"
]

train_ds = tf.keras.utils.image_dataset_from_directory(
    IMAGES_DIR,
    labels="inferred",
    label_mode="categorical",
    class_names=CLASS_NAMES,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    subset="training",
    seed=123
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    IMAGES_DIR,
    labels="inferred",
    label_mode="categorical",
    class_names=CLASS_NAMES,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    subset="validation",
    seed=123
)

# Sauvegarde de l'ordre exact des classes
class_names_path = os.path.join(MODELS_DIR, "class_names.json")

with open(class_names_path, "w", encoding="utf-8") as f:
    json.dump(CLASS_NAMES, f, ensure_ascii=False, indent=2)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

# ======================
# DATA AUGMENTATION
# ======================

data_augmentation = models.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# ======================
# MODÈLE CNN : MobileNetV2
# ======================

base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),
    data_augmentation,

    # Remplace Lambda(preprocess_input)
    # Transforme les pixels [0,255] vers [-1,1]
    layers.Rescaling(scale=1./127.5, offset=-1),

    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(4, activation="softmax")
])

# ======================
# COMPILATION
# ======================

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ======================
# ENTRAÎNEMENT
# ======================

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10
)

# ======================
# SAUVEGARDE
# ======================

model_path = os.path.join(MODELS_DIR, "phytovision_mobilenetv2.keras")
model.save(model_path)

print("\nModèle sauvegardé ici :")
print(model_path)

print("\nClasses sauvegardées ici :")
print(class_names_path)