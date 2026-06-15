import cv2
import numpy as np
import matplotlib.pyplot as plt

# ==================================
# IMAGE A TESTER
# ==================================

IMAGE_PATH = r"C:\Users\PC\Documents\Projet IA\Maize\Tache_grise\leaf spot146_.jpg"

# ==================================
# CHARGEMENT
# ==================================

image = cv2.imread(IMAGE_PATH)

if image is None:
    print("Impossible de charger l'image")
    exit()

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# ==================================
# K-MEANS
# ==================================

pixels = image_rgb.reshape((-1, 3))

pixels = np.float32(pixels)

criteria = (
    cv2.TERM_CRITERIA_EPS +
    cv2.TERM_CRITERIA_MAX_ITER,
    100,
    0.2
)

K = 3

_, labels, centers = cv2.kmeans(
    pixels,
    K,
    None,
    criteria,
    10,
    cv2.KMEANS_RANDOM_CENTERS
)

centers = np.uint8(centers)

segmented = centers[labels.flatten()]
segmented = segmented.reshape(image_rgb.shape)

# ==================================
# DETECTION ZONE MALADE
# ==================================

cluster_sizes = []

for i in range(K):
    cluster_sizes.append(np.sum(labels == i))

malade_cluster = np.argmin(cluster_sizes)

malade_pixels = np.sum(labels == malade_cluster)

total_pixels = image_rgb.shape[0] * image_rgb.shape[1]

severite = (malade_pixels / total_pixels) * 100

# ==================================
# NIVEAU
# ==================================

if severite < 10:
    niveau = "Faible"

elif severite < 30:
    niveau = "Modérée"

elif severite < 60:
    niveau = "Élevée"

else:
    niveau = "Critique"

# ==================================
# RESULTATS
# ==================================

print("\n===== ANALYSE DE SÉVÉRITÉ =====")

print(f"Sévérité : {severite:.2f}%")

print("Niveau :", niveau)

# ==================================
# VISUALISATION
# ==================================

plt.figure(figsize=(12,6))

plt.subplot(1,2,1)
plt.imshow(image_rgb)
plt.title("Image originale")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(segmented)
plt.title("Segmentation K-Means")
plt.axis("off")

plt.show()