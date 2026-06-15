"""
=============================================================
  Module : recommandation.py
=============================================================
  Interface entre le MDP et le pipeline PhytoVision.

  Reçoit (maladie_id, severite_id) issus du CNN + K-Means,
  et retourne la recommandation (action_id) à insérer dans
  la table Diagnostic de la base de données.
=============================================================
"""

from mdp.etats import ETATS, obtenir_etat
from mdp.actions import ACTIONS


def recommander(maladie_id: int, severite_id: int | None, politique: dict) -> dict:
    """
    Fournit la recommandation phytosanitaire pour un diagnostic donné.

    Paramètres
    ----------
    maladie_id  : int
        Identifiant de la maladie détectée par le CNN (table Maladie).
    severite_id : int | None
        Identifiant de sévérité estimé par K-Means (table Sévérité).
        None si maladie_id = 0 (Healthy).
    politique   : dict
        Politique optimale {etat: action} issue de value_iteration().

    Retourne
    --------
    dict
        Dictionnaire prêt à être utilisé pour mettre à jour
        la table Diagnostic :
        {
            "etat":        identifiant d'état (ex. "S2"),
            "etat_nom":    nom lisible de l'état,
            "maladie_id":  identifiant maladie (entrée),
            "severite_id": identifiant sévérité (entrée),
            "action_id":   identifiant action (table Action),
            "action_nom":  nom lisible de l'action recommandée,
        }

    Lève
    ----
    ValueError
        Si la combinaison (maladie_id, severite_id) ne correspond
        à aucun état défini.
    """
    etat = obtenir_etat(maladie_id, severite_id)
    if etat is None:
        raise ValueError(
            f"État inconnu : maladie_id={maladie_id}, severite_id={severite_id}"
        )

    action_cle  = politique[etat]
    action_info = ACTIONS[action_cle]

    return {
        "etat":        etat,
        "etat_nom":    ETATS[etat]["nom"],
        "maladie_id":  maladie_id,
        "severite_id": severite_id,
        "action_id":   action_info["action_id"],
        "action_nom":  action_info["nom"],
    }
