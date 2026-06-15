"""
=============================================================
  Module : affichage.py
=============================================================
  Fonctions d'affichage des résultats du MDP PhytoVision :
    - la politique optimale (table récapitulative)
    - une recommandation individuelle (carte de diagnostic)
=============================================================
"""

from mdp.etats import LISTE_ETATS, ETATS
from mdp.actions import ACTIONS


def afficher_politique(politique: dict, V: dict) -> None:
    """
    Affiche la politique optimale et la valeur de chaque état
    sous forme de tableau.

    Paramètres
    ----------
    politique : dict {etat: action optimale}
    V         : dict {etat: valeur optimale}
    """
    sep = "─" * 72
    print(f"\n{sep}")
    print(f"  {'ÉTAT':<32} {'ACTION OPTIMALE':<26} {'ACTION_ID':>9}  {'V(s)':>8}")
    print(sep)

    for s in LISTE_ETATS:
        a     = politique[s]
        nom_e = ETATS[s]["nom"]
        nom_a = ACTIONS[a]["nom"]
        aid   = ACTIONS[a]["action_id"]
        val   = V[s]
        print(f"  {s} — {nom_e:<28} {nom_a:<26} {aid:>9}  {val:>8.1f}")

    print(sep)


def afficher_recommandation(res: dict) -> None:
    """
    Affiche une recommandation individuelle sous forme de carte.

    Paramètres
    ----------
    res : dict
        Sortie de recommandation.recommander()
    """
    print(f"""
  ┌─ Diagnostic PhytoVision ──────────────────────────────────┐
  │  État détecté  : {res['etat']} — {res['etat_nom']:<39}│
  │  Maladie ID    : {res['maladie_id']:<52}│
  │  Sévérité ID   : {str(res['severite_id']):<52}│
  │  ─────────────────────────────────────────────────────────│
  │  Action ID     : {res['action_id']:<52}│
  │  Recommandation: {res['action_nom']:<52}│
  └───────────────────────────────────────────────────────────┘""")
