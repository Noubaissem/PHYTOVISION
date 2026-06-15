"""
=============================================================
  Module : value_iteration.py
=============================================================
  Algorithme de Value Iteration pour le MDP PhytoVision.

  Calcule :
    - V(s)      : la valeur optimale de chaque état
    - politique : l'action optimale pour chaque état

  Formule de mise à jour :
      Q(s,a) = R(s,a) + γ · Σ P(s'|s,a) · V(s')
      V(s)   = max_a Q(s,a)
=============================================================
"""

from mdp.etats import LISTE_ETATS
from mdp.actions import LISTE_ACTIONS
from mdp.recompenses import recompense


def value_iteration(P: dict, gamma: float = 0.9, theta: float = 1e-6,
                     verbose: bool = True) -> tuple:
    """
    Exécute l'algorithme de Value Iteration.

    Paramètres
    ----------
    P       : table de transition P[s][a][s'] = probabilité
    gamma   : facteur d'actualisation (0 < gamma <= 1)
    theta   : seuil de convergence
    verbose : afficher le nombre d'itérations à la convergence

    Retourne
    --------
    V                : dict {etat: valeur optimale}
    politique        : dict {etat: action optimale}
    historique_delta : list des deltas successifs (suivi de convergence)
    """

    # Initialisation des valeurs à zéro
    V = {s: 0.0 for s in LISTE_ETATS}
    historique_delta = []
    iteration = 0

    while True:
        delta = 0.0
        iteration += 1
        V_nouveau = V.copy()

        for s in LISTE_ETATS:
            valeurs_actions = []
            for a in LISTE_ACTIONS:
                q = recompense(s, a) + gamma * sum(
                    prob * V[s_suivant]
                    for s_suivant, prob in P[s][a].items()
                )
                valeurs_actions.append(q)

            V_nouveau[s] = max(valeurs_actions)
            delta = max(delta, abs(V_nouveau[s] - V[s]))

        V = V_nouveau
        historique_delta.append(delta)

        if delta < theta:
            if verbose:
                print(f"  Convergence atteinte en {iteration} itérations (Δ = {delta:.2e})")
            break

    # Extraction de la politique optimale (un passage supplémentaire)
    politique = {}
    for s in LISTE_ETATS:
        valeurs_actions = {}
        for a in LISTE_ACTIONS:
            q = recompense(s, a) + gamma * sum(
                prob * V[s_suivant]
                for s_suivant, prob in P[s][a].items()
            )
            valeurs_actions[a] = q
        politique[s] = max(valeurs_actions, key=valeurs_actions.get)

    return V, politique, historique_delta
