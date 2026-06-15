"""
=============================================================
  Module : etats.py
=============================================================
  Définition de l'espace des états S du MDP PhytoVision.

  Chaque état représente la situation sanitaire de la plante,
  construite à partir de :
      - la maladie détectée par le CNN  (maladie_id)
      - la sévérité estimée par K-Means (severite_id)

  Cohérent avec les tables "Maladie" et "Sévérité" de la BDD.
=============================================================
"""

# -------------------------------------------------------------
# Définition des 10 états
# -------------------------------------------------------------
ETATS = {
    "S0": {"nom": "Healthy",                      "maladie_id": 0, "severite_id": None},
    "S1": {"nom": "Common Rust Faible",           "maladie_id": 1, "severite_id": 1},
    "S2": {"nom": "Common Rust Moyenne",          "maladie_id": 1, "severite_id": 2},
    "S3": {"nom": "Common Rust Élevée",           "maladie_id": 1, "severite_id": 3},
    "S4": {"nom": "Northern Leaf Blight Faible",  "maladie_id": 2, "severite_id": 1},
    "S5": {"nom": "Northern Leaf Blight Moyenne", "maladie_id": 2, "severite_id": 2},
    "S6": {"nom": "Northern Leaf Blight Élevée",  "maladie_id": 2, "severite_id": 3},
    "S7": {"nom": "Gray Leaf Spot Faible",        "maladie_id": 3, "severite_id": 1},
    "S8": {"nom": "Gray Leaf Spot Moyenne",       "maladie_id": 3, "severite_id": 2},
    "S9": {"nom": "Gray Leaf Spot Élevée",        "maladie_id": 3, "severite_id": 3},
}

# Liste ordonnée des identifiants d'états : ["S0", "S1", ..., "S9"]
LISTE_ETATS = list(ETATS.keys())

# Nombre total d'états (= 10)
N_ETATS = len(LISTE_ETATS)

# Dictionnaire {etat: index} utile pour les matrices/tableaux
IDX_ETAT = {s: i for i, s in enumerate(LISTE_ETATS)}


# -------------------------------------------------------------
# Conversion (maladie_id, severite_id) -> état (Sx)
# -------------------------------------------------------------
def obtenir_etat(maladie_id: int, severite_id: int | None) -> str | None:
    """
    Convertit un couple (maladie_id, severite_id) issu du pipeline
    CNN + K-Means en identifiant d'état du MDP (ex. "S2").

    Paramètres
    ----------
    maladie_id  : int
        0 = Healthy, 1 = Common Rust, 2 = Northern Leaf Blight,
        3 = Gray Leaf Spot  (table Maladie)
    severite_id : int | None
        1 = Faible, 2 = Moyenne, 3 = Élevée  (table Sévérité)
        None si maladie_id = 0 (Healthy)

    Retourne
    --------
    str | None
        Identifiant d'état (ex. "S2"), ou None si la combinaison
        n'existe pas dans l'espace des états.
    """
    if maladie_id == 0:
        return "S0"

    for sid, info in ETATS.items():
        if info["maladie_id"] == maladie_id and info["severite_id"] == severite_id:
            return sid

    return None
