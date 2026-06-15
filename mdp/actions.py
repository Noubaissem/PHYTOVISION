"""
=============================================================
  Module : actions.py
=============================================================
  Définition de l'espace des actions A du MDP PhytoVision.

  Chaque action correspond à une recommandation phytosanitaire.
  Cohérent avec la table "Action" de la base de données.
=============================================================
"""

# -------------------------------------------------------------
# Définition des 4 actions
# -------------------------------------------------------------
ACTIONS = {
    "A1": {"nom": "Surveillance",         "action_id": 1, "cout": 0},
    "A2": {"nom": "Traitement préventif", "action_id": 2, "cout": -5},
    "A3": {"nom": "Traitement curatif",   "action_id": 3, "cout": -15},
    "A4": {"nom": "Élimination du foyer", "action_id": 4, "cout": -40},
}

# Liste ordonnée des identifiants d'actions : ["A1", "A2", "A3", "A4"]
LISTE_ACTIONS = list(ACTIONS.keys())

# Nombre total d'actions (= 4)
N_ACTIONS = len(LISTE_ACTIONS)

# Dictionnaire {action: index} utile pour les matrices/tableaux
IDX_ACTION = {a: i for i, a in enumerate(LISTE_ACTIONS)}
