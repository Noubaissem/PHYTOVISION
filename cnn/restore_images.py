import os
import shutil
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATASET_DIR = os.path.join(BASE_DIR, "dataset")
BAD_DIR = os.path.join(PROJECT_DIR, "bad_images")
MAIZE_DIR = os.path.join(PROJECT_DIR, "Maize")

label_map = {
    0: "Sain",
    1: "Virus_de_la_strie",
    2: "Brulure_foliaire",
    3: "Tache_grise"
}

csv_files = ["train.csv", "val.csv", "test.csv"]

restored = 0
missing = 0

for csv_file in csv_files:
    csv_path = os.path.join(DATASET_DIR, csv_file)

    if not os.path.exists(csv_path):
        continue

    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        filename = row["image"]
        label = label_map[row["maladie_id"]]

        source = os.path.join(BAD_DIR, filename)
        destination_dir = os.path.join(MAIZE_DIR, label)
        destination = os.path.join(destination_dir, filename)

        os.makedirs(destination_dir, exist_ok=True)

        if os.path.exists(source):
            shutil.move(source, destination)
            restored += 1
        else:
            missing += 1

print("Images restaurées :", restored)
print("Images non trouvées dans bad_images :", missing)
print("Restauration terminée.")