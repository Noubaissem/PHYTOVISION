import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
IMAGES_DIR = os.path.join(PROJECT_DIR, "Maize")

bad_files = []

for root, dirs, files in os.walk(IMAGES_DIR):
    for file in files:
        path = os.path.join(root, file)

        try:
            with Image.open(path) as img:
                img.verify()
        except Exception:
            bad_files.append(path)

print("Images corrompues ou invalides trouvées :", len(bad_files))

for path in bad_files:
    print(path)

# Déplacer les mauvais fichiers dans un dossier à part
BAD_DIR = os.path.join(PROJECT_DIR, "bad_images")
os.makedirs(BAD_DIR, exist_ok=True)

for path in bad_files:
    filename = os.path.basename(path)
    new_path = os.path.join(BAD_DIR, filename)

    try:
        os.replace(path, new_path)
    except Exception as e:
        print("Impossible de déplacer :", path, e)

print("Nettoyage terminé.")