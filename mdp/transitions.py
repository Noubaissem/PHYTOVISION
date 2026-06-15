"""
=============================================================
  Module : transitions.py
=============================================================
  Fonction de transition P(s' | s, a) du MDP PhytoVision.

  Modélise l'évolution probable de la maladie après
  l'application d'une action.

  Règle générale :
    - Action adaptée à la sévérité  -> forte proba de guérison
    - Action insuffisante           -> maintien / aggravation
    - Surveillance sur une maladie  -> progression probable

  Ces probabilités sont des hypothèses de travail, à affiner
  avec la littérature agronomique et l'encadrement du projet.
=============================================================
"""

from mdp.etats import LISTE_ETATS
from mdp.actions import LISTE_ACTIONS


def construire_transitions() -> dict:
    """
    Construit la table de transition complète.

    Retourne
    --------
    dict
        P[s][a] = { s_suivant: probabilité, ... }
        avec sum(P[s][a].values()) == 1.0 pour tout (s, a)
    """

    # Initialisation : par défaut, on reste dans le même état
    P = {s: {a: {s: 1.0} for a in LISTE_ACTIONS} for s in LISTE_ETATS}

    # --- S0 : Healthy (état absorbant) ---
    for a in LISTE_ACTIONS:
        P["S0"][a] = {"S0": 1.0}

    # --- S1 : Common Rust Faible ---
    P["S1"]["A1"] = {"S1": 0.60, "S2": 0.30, "S3": 0.10}   # Surveillance
    P["S1"]["A2"] = {"S0": 0.70, "S1": 0.20, "S2": 0.10}   # Préventif
    P["S1"]["A3"] = {"S0": 0.80, "S1": 0.15, "S2": 0.05}   # Curatif
    P["S1"]["A4"] = {"S0": 0.90, "S1": 0.10}                # Élimination

    # --- S2 : Common Rust Moyenne ---
    P["S2"]["A1"] = {"S2": 0.50, "S3": 0.40, "S1": 0.10}
    P["S2"]["A2"] = {"S1": 0.50, "S2": 0.35, "S3": 0.15}
    P["S2"]["A3"] = {"S0": 0.30, "S1": 0.60, "S2": 0.10}
    P["S2"]["A4"] = {"S0": 0.70, "S1": 0.20, "S2": 0.10}

    # --- S3 : Common Rust Élevée ---
    P["S3"]["A1"] = {"S3": 0.80, "S2": 0.20}
    P["S3"]["A2"] = {"S3": 0.60, "S2": 0.30, "S1": 0.10}
    P["S3"]["A3"] = {"S2": 0.50, "S1": 0.30, "S3": 0.20}
    P["S3"]["A4"] = {"S0": 0.50, "S1": 0.30, "S2": 0.20}

    # --- S4 : Northern Leaf Blight Faible ---
    P["S4"]["A1"] = {"S4": 0.55, "S5": 0.35, "S6": 0.10}
    P["S4"]["A2"] = {"S0": 0.65, "S4": 0.25, "S5": 0.10}
    P["S4"]["A3"] = {"S0": 0.75, "S4": 0.20, "S5": 0.05}
    P["S4"]["A4"] = {"S0": 0.88, "S4": 0.12}

    # --- S5 : Northern Leaf Blight Moyenne ---
    P["S5"]["A1"] = {"S5": 0.50, "S6": 0.40, "S4": 0.10}
    P["S5"]["A2"] = {"S4": 0.45, "S5": 0.40, "S6": 0.15}
    P["S5"]["A3"] = {"S0": 0.28, "S4": 0.58, "S5": 0.14}
    P["S5"]["A4"] = {"S0": 0.68, "S4": 0.22, "S5": 0.10}

    # --- S6 : Northern Leaf Blight Élevée ---
    P["S6"]["A1"] = {"S6": 0.82, "S5": 0.18}
    P["S6"]["A2"] = {"S6": 0.62, "S5": 0.28, "S4": 0.10}
    P["S6"]["A3"] = {"S5": 0.48, "S4": 0.32, "S6": 0.20}
    P["S6"]["A4"] = {"S0": 0.48, "S4": 0.32, "S5": 0.20}

    # --- S7 : Gray Leaf Spot Faible ---
    P["S7"]["A1"] = {"S7": 0.58, "S8": 0.32, "S9": 0.10}
    P["S7"]["A2"] = {"S0": 0.68, "S7": 0.22, "S8": 0.10}
    P["S7"]["A3"] = {"S0": 0.78, "S7": 0.17, "S8": 0.05}
    P["S7"]["A4"] = {"S0": 0.90, "S7": 0.10}

    # --- S8 : Gray Leaf Spot Moyenne ---
    P["S8"]["A1"] = {"S8": 0.52, "S9": 0.38, "S7": 0.10}
    P["S8"]["A2"] = {"S7": 0.42, "S8": 0.42, "S9": 0.16}
    P["S8"]["A3"] = {"S0": 0.30, "S7": 0.55, "S8": 0.15}
    P["S8"]["A4"] = {"S0": 0.65, "S7": 0.25, "S8": 0.10}

    # --- S9 : Gray Leaf Spot Élevée ---
    P["S9"]["A1"] = {"S9": 0.80, "S8": 0.20}
    P["S9"]["A2"] = {"S9": 0.62, "S8": 0.28, "S7": 0.10}
    P["S9"]["A3"] = {"S8": 0.50, "S7": 0.30, "S9": 0.20}
    P["S9"]["A4"] = {"S0": 0.50, "S7": 0.30, "S8": 0.20}

    return P
