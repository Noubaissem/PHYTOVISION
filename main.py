"""
=============================================================
  Module : main.py
=============================================================
  Point d'entrée du module MDP de PhytoVision.

  Pipeline :
    1. Construction de la table de transition P(s'|s,a)
    2. Calcul de la politique optimale par Value Iteration
    3. Affichage de la politique
    4. Tests de recommandation sur des diagnostics types

  Exécution :
      python -m mdp.main
  (à lancer depuis le dossier qui CONTIENT le dossier "mdp/")
=============================================================
"""

from mdp.transitions import construire_transitions
from mdp.value_iteration import value_iteration
from mdp.recommandation import recommander
from mdp.affichage import afficher_politique, afficher_recommandation


def main() -> dict:
    """
    Exécute le pipeline complet du MDP et retourne la politique optimale.

    Retourne
    --------
    dict
        Politique optimale {etat: action}, réutilisable par
        d'autres modules (ex. API, interface CNN + K-Means).
    """

    print("\n" + "=" * 72)
    print("  PHYTOVISION — Calcul de la politique MDP (Value Iteration)")
    print("=" * 72)

    # 1. Construction des transitions
    print("\n[1/3] Construction de la table de transition...")
    P = construire_transitions()

    # 2. Value Iteration
    print("[2/3] Exécution de Value Iteration (γ=0.9, θ=1e-6)...")
    V, politique, historique = value_iteration(P, gamma=0.9, theta=1e-6)

    # 3. Affichage de la politique optimale
    print("\n[3/3] Politique optimale calculée :")
    afficher_politique(politique, V)

    # 4. Tests : simulation de diagnostics réels
    print("\n" + "=" * 72)
    print("  TESTS — Recommandations pour différents diagnostics")
    print("=" * 72)

    cas_tests = [
        (0, None, "Plante saine"),
        (1, 1,    "Common Rust Faible"),
        (1, 2,    "Common Rust Moyenne"),
        (1, 3,    "Common Rust Élevée"),
        (2, 1,    "Northern Leaf Blight Faible"),
        (2, 3,    "Northern Leaf Blight Élevée"),
        (3, 2,    "Gray Leaf Spot Moyenne"),
        (3, 3,    "Gray Leaf Spot Élevée"),
    ]

    for maladie_id, severite_id, description in cas_tests:
        print(f"\n  Cas : {description}")
        res = recommander(maladie_id, severite_id, politique)
        afficher_recommandation(res)

    print("\n" + "=" * 72)
    print("  Intégration BDD : insérer res['action_id'] dans Diagnostic.action_id")
    print("=" * 72 + "\n")

    return politique


if __name__ == "__main__":
    main()
