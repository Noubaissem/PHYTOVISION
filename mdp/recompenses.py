"""
=============================================================
  Module : recompenses.py
=============================================================
  Fonction de récompense R(s, a) du MDP PhytoVision.

  R(s, a) = récompense_état(s) + coût_action(a)

  - La récompense d'état traduit la santé de la culture.
  - Le coût d'action traduit l'effort/dépense liée à l'action.
=============================================================
"""

from mdp.actions import ACTIONS


# -------------------------------------------------------------
# Récompense liée à l'état (santé de la plante)
# -------------------------------------------------------------
RECOMPENSE_ETAT = {
    "S0": +100,   # Healthy
    "S1": +40,    # Common Rust   - Faible
    "S2": -20,    # Common Rust   - Moyenne
    "S3": -80,    # Common Rust   - Élevée
    "S4": +40,    # NLB           - Faible
    "S5": -20,    # NLB           - Moyenne
    "S6": -80,    # NLB           - Élevée
    "S7": +40,    # Gray Leaf Spot- Faible
    "S8": -20,    # Gray Leaf Spot- Moyenne
    "S9": -80,    # Gray Leaf Spot- Élevée
}


# -------------------------------------------------------------
# Fonction de récompense globale R(s, a)
# -------------------------------------------------------------
def recompense(etat: str, action: str) -> float:
    """
    Calcule la récompense immédiate R(s, a).

    Paramètres
    ----------
    etat   : identifiant d'état (ex. "S2")
    action : identifiant d'action (ex. "A3")

    Retourne
    --------
    float : récompense_état(s) + coût_action(a)
    """
    return RECOMPENSE_ETAT[etat] + ACTIONS[action]["cout"]
