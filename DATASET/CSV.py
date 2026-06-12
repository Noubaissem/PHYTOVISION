import os
import cv2
import uuid
import warnings
import numpy as np
import pandas as pd
import random
from PIL import Image
from skimage.feature import graycomatrix, graycoprops
from sklearn.model_selection import train_test_split
import albumentations as A

# ── Configuration ─────────────────────────────────
CLASS_MAP = {
    "Sain":               {"maladie_id": 0, "etat_id": 0},
    "Virus_de_la_strie":  {"maladie_id": 1, "etat_id": 1},
    "Brulure_foliaire":   {"maladie_id": 2, "etat_id": 1},
    "Tache_grise":        {"maladie_id": 3, "etat_id": 1},
}
CULTURE_ID   = 1     # Maïs
TARGET_COUNT = 1500  # Target per class → 4 × 1500 = 6000 total
RANDOM_SEED  = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# ── Augmentation pipeline ─────────────────────────
AUGMENTOR = A.Compose([
    A.Rotate(limit=30, p=0.8),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.3),
    A.RandomBrightnessContrast(
        brightness_limit=0.4,
        contrast_limit=0.3,
        p=0.7
    ),
    A.HueSaturationValue(
        hue_shift_limit=15,
        sat_shift_limit=20,
        val_shift_limit=10,
        p=0.6
    ),
    A.GaussNoise(p=0.4),
    A.Blur(blur_limit=3, p=0.2),
])


# ── Step 1 — Augment minority classes ─────────────
def augment_class(class_dir, target_count):
    existing = [
        f for f in os.listdir(class_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]
    current = len(existing)
    needed  = target_count - current

    if needed <= 0:
        print(f"    Already has {current} images — no augmentation needed")
        return

    print(f"    Has {current} images — generating {needed} more...")
    generated = 0

    while generated < needed:
        src_file = existing[generated % len(existing)]
        src_path = os.path.join(class_dir, src_file)

        img = cv2.imread(src_path)
        if img is None:
            generated += 1
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result  = AUGMENTOR(image=img_rgb)["image"]

        out_name = f"AUG_{uuid.uuid4().hex[:8]}.jpg"
        out_path = os.path.join(class_dir, out_name)
        cv2.imwrite(
            out_path,
            cv2.cvtColor(result, cv2.COLOR_RGB2BGR),
            [cv2.IMWRITE_JPEG_QUALITY, 95]
        )
        generated += 1

        if generated % 100 == 0:
            print(f"      → {generated}/{needed} generated")

    final = len([
        f for f in os.listdir(class_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])
    print(f"    ✅ Done — {final} images in folder")


def run_augmentation(data_dir, target_count):
    print("=" * 50)
    print(f"STEP 1 — Augmenting classes to {target_count} images each")
    print("=" * 50)
    for class_name in CLASS_MAP.keys():
        class_dir = os.path.join(data_dir, class_name)
        if not os.path.isdir(class_dir):
            print(f"⚠  Folder not found: {class_dir}")
            continue
        print(f"\n  {class_name}:")
        augment_class(class_dir, target_count)
    print()


# ── Step 2 — Feature extraction for Naïve Bayes ───
def extract_features(img_path):
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Cannot read: {img_path}")

    img_rgb         = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_hsv         = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_resized     = cv2.resize(img_rgb, (224, 224))
    img_hsv_resized = cv2.resize(img_hsv, (224, 224))
    img_gray        = cv2.cvtColor(
        cv2.resize(img, (224, 224)), cv2.COLOR_BGR2GRAY
    )

    r_mean = img_resized[:, :, 0].mean()
    g_mean = img_resized[:, :, 1].mean()
    b_mean = img_resized[:, :, 2].mean()
    h_mean = img_hsv_resized[:, :, 0].mean()
    s_mean = img_hsv_resized[:, :, 1].mean()
    v_mean = img_hsv_resized[:, :, 2].mean()

    pixels = img_resized.reshape(-1, 3)
    brown_ratio = np.sum(
        (pixels[:, 0] > 120) &
        (pixels[:, 1] > 60) & (pixels[:, 1] < 130) &
        (pixels[:, 2] < 80)
    ) / len(pixels)
    yellow_ratio = np.sum(
        (pixels[:, 0] > 150) &
        (pixels[:, 1] > 150) &
        (pixels[:, 2] < 80)
    ) / len(pixels)
    dark_ratio = np.sum(
        (pixels[:, 0] < 50) &
        (pixels[:, 1] < 50) &
        (pixels[:, 2] < 50)
    ) / len(pixels)

    glcm = graycomatrix(
        img_gray, distances=[1], angles=[0],
        levels=256, symmetric=True, normed=True
    )
    contrast    = graycoprops(glcm, 'contrast')[0, 0]
    energy      = graycoprops(glcm, 'energy')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
    correlation = graycoprops(glcm, 'correlation')[0, 0]

    return {
        "r_mean":       round(float(r_mean), 4),
        "g_mean":       round(float(g_mean), 4),
        "b_mean":       round(float(b_mean), 4),
        "h_mean":       round(float(h_mean), 4),
        "s_mean":       round(float(s_mean), 4),
        "v_mean":       round(float(v_mean), 4),
        "brown_ratio":  round(float(brown_ratio), 4),
        "yellow_ratio": round(float(yellow_ratio), 4),
        "dark_ratio":   round(float(dark_ratio), 4),
        "contrast":     round(float(contrast), 4),
        "energy":       round(float(energy), 4),
        "homogeneity":  round(float(homogeneity), 4),
        "correlation":  round(float(correlation), 4),
    }


# ── Step 3 — Build both CSVs ──────────────────────
def build_datasets(data_dir, output_dir):
    print("=" * 50)
    print("STEP 2 — Building CSV datasets")
    print("=" * 50)

    os.makedirs(output_dir, exist_ok=True)
    cnn_rows = []
    nb_rows  = []
    skipped  = 0

    for class_name, ids in CLASS_MAP.items():
        class_dir = os.path.join(data_dir, class_name)
        if not os.path.exists(class_dir):
            print(f"⚠  Folder not found: {class_dir}")
            continue

        images = [
            f for f in os.listdir(class_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        print(f"\n  Processing {class_name}: {len(images)} images")

        for i, img_file in enumerate(images):
            img_path = os.path.join(class_dir, img_file)
            if (i + 1) % 200 == 0:
                print(f"    → {i + 1}/{len(images)}")

            cnn_rows.append({
                "image":      img_file,
                "culture_id": CULTURE_ID,
                "maladie_id": ids["maladie_id"],
                "etat_id":    ids["etat_id"],
            })
            try:
                features = extract_features(img_path)
                nb_rows.append({
                    "image_name": img_file,
                    **features,
                    "maladie_id": ids["maladie_id"],
                })
            except Exception as e:
                skipped += 1
                print(f"    ⚠  Skipping {img_file}: {e}")

    cnn_df = pd.DataFrame(cnn_rows)
    nb_df  = pd.DataFrame(nb_rows)

    cnn_path = os.path.join(output_dir, "dataset_cnn.csv")
    nb_path  = os.path.join(output_dir, "dataset_naive_bayes.csv")
    cnn_df.to_csv(cnn_path, index=False)
    nb_df.to_csv(nb_path,   index=False)

    print("\n" + "=" * 50)
    print("RESULTS — CSV BUILD")
    print("=" * 50)
    print(f"  ✅ CNN CSV          : {len(cnn_df)} rows")
    print(f"  ✅ Naïve Bayes CSV  : {len(nb_df)} rows")
    print(f"  ⚠  NB rows skipped  : {skipped}")

    labels = {0:"Sain", 1:"Virus_strie", 2:"Brulure", 3:"Tache_grise"}
    print("\n  Class distribution:")
    dist = cnn_df.groupby("maladie_id").size()
    for mid, count in dist.items():
        pct = count / len(cnn_df) * 100
        bar = "█" * int(pct / 2)
        print(f"    {labels.get(mid,'?'):15s}: "
              f"{count:5d} ({pct:5.1f}%) {bar}")

    return cnn_df, nb_df


# ── Step 4 — Split into Train / Val / Test ────────
def split_dataset(splits_dir, train_ratio=0.70,
                  val_ratio=0.15, test_ratio=0.15):
    print("\n" + "=" * 50)
    print("STEP 3 — Splitting dataset")
    print("=" * 50)

    csv_path = os.path.join(splits_dir, "dataset_cnn.csv")
    df = pd.read_csv(csv_path)
    print(f"\n  Total images loaded : {len(df)}")

    # Split 1: Train vs (Val + Test)
    train_df, temp_df = train_test_split(
        df,
        test_size=(val_ratio + test_ratio),
        stratify=df["maladie_id"],
        random_state=RANDOM_SEED
    )

    # Split 2: Val vs Test (equal halves of temp)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        stratify=temp_df["maladie_id"],
        random_state=RANDOM_SEED
    )

    # Save
    train_path = os.path.join(splits_dir, "train.csv")
    val_path   = os.path.join(splits_dir, "val.csv")
    test_path  = os.path.join(splits_dir, "test.csv")
    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path,     index=False)
    test_df.to_csv(test_path,   index=False)

    # Summary
    labels = {0:"Sain", 1:"Virus_strie", 2:"Brulure", 3:"Tache_grise"}

    print(f"\n  {'Split':<12} {'Images':>8} {'%':>8}")
    print(f"  {'-'*30}")
    print(f"  {'Train':<12} {len(train_df):>8} "
          f"{len(train_df)/len(df)*100:>7.1f}%")
    print(f"  {'Validation':<12} {len(val_df):>8} "
          f"{len(val_df)/len(df)*100:>7.1f}%")
    print(f"  {'Test':<12} {len(test_df):>8} "
          f"{len(test_df)/len(df)*100:>7.1f}%")
    print(f"  {'-'*30}")
    print(f"  {'TOTAL':<12} {len(df):>8} {'100.0%':>8}")

    print(f"\n  Class distribution per split:")
    print(f"  {'Class':<16} {'Train':>7} {'Val':>7} {'Test':>7}")
    print(f"  {'-'*40}")
    for mid in sorted(df["maladie_id"].unique()):
        t = len(train_df[train_df["maladie_id"] == mid])
        v = len(val_df[val_df["maladie_id"]     == mid])
        e = len(test_df[test_df["maladie_id"]   == mid])
        print(f"  {labels.get(mid,str(mid)):<16} {t:>7} {v:>7} {e:>7}")

    print(f"\n  ✅ train.csv → {train_path}")
    print(f"  ✅ val.csv   → {val_path}")
    print(f"  ✅ test.csv  → {test_path}")
    print(f"\n  ⚠  IMPORTANT: Do not open or use test.csv")
    print(f"     until final model evaluation.")

    return train_df, val_df, test_df


# ── Main ──────────────────────────────────────────
if __name__ == "__main__":

    DATA_DIR   = "Maize"
    OUTPUT_DIR = "data/splits"

    # Step 1: Augment minority classes
    run_augmentation(DATA_DIR, TARGET_COUNT)

    # Step 2: Build CNN and Naïve Bayes CSVs
    cnn_df, nb_df = build_datasets(DATA_DIR, OUTPUT_DIR)

    # Step 3: Split into Train / Val / Test
    train_df, val_df, test_df = split_dataset(OUTPUT_DIR)

    print("\n" + "=" * 50)
    print("✅ ALL STEPS COMPLETE")
    print("=" * 50)
    print(f"  Total images : {len(cnn_df)}")
    print(f"  Train        : {len(train_df)}")
    print(f"  Validation   : {len(val_df)}")
    print(f"  Test         : {len(test_df)}")
    print(f"\n  Files in {OUTPUT_DIR}/:")
    print(f"  → dataset_cnn.csv")
    print(f"  → dataset_naive_bayes.csv")
    print(f"  → train.csv")
    print(f"  → val.csv")
    print(f"  → test.csv  ⚠ sealed until final evaluation")