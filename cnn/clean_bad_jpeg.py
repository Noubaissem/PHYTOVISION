import os
import shutil
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

MAIZE_DIR = os.path.join(PROJECT_DIR, "Maize")
BAD_DIR = os.path.join(PROJECT_DIR, "bad_jpeg_images")

os.makedirs(BAD_DIR, exist_ok=True)

bad_files = []
total = 0

for root, dirs, files in os.walk(MAIZE_DIR):
    for file in files:
        path = os.path.join(root, file)
        total += 1

        try:
            with Image.open(path) as img:
                img.load()
        except Exception as e:
            bad_files.append((path, str(e)))

print("Total fichiers vérifiés :", total)
print("Images JPEG invalides trouvées :", len(bad_files))

for path, error in bad_files:
    print(path, "=>", error)

for path, error in bad_files:
    relative_path = os.path.relpath(path, MAIZE_DIR)
    destination = os.path.join(BAD_DIR, relative_path)

    os.makedirs(os.path.dirname(destination), exist_ok=True)
    shutil.move(path, destination)

print("Images invalides déplacées dans :", BAD_DIR)
print("Nettoyage terminé.")