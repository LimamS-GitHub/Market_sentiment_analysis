# 🚶‍♂️ Vers une stratégie de trading simple

À partir des signaux calibrés à l'étape précédente, nous allons :

Construire une stratégie d’achat/vente simple, en exploitant les seuils de sentiment.
Tester sa rentabilité sur les données de 2022.
Puis ajuster automatiquement les paramètres pour maximiser la performance de la stratégie.

## Prototype d’une stratégie simple

À partir des signaux de sentiment filtrés et lissés, nous testons une stratégie rudimentaire :

- **Achat** si le sentiment est supérieur à un certain seuil (ex. : 0.4)
- **Sortie du marché** si le sentiment descend en dessous d’un seuil négatif (ex. : -0.4)

Chaque décision est prise à la clôture du jour, en fonction du score de sentiment observé dans la même journée.
On suppose que les données de sentiment ont été collectées et traitées suffisamment tôt pour pouvoir être utilisées avant la fin de séance.


> Avec cette stratégie rudimentaire, on obtient une performance annuelle de +0.67 % sans frais de transaction.
---

## Recherche d’hyperparamètres

Pour améliorer les performances de la stratégie, nous effectuons une **recherche exhaustive (grid search)** sur les éléments suivants :

- Le **modèle de sentiment** utilisé (parmi les 4 testés),
- Le **niveau de lissage** appliqué au score (fenêtre mobile de 1 à 7 jours),
- Les **seuils d’achat et de vente**, explorés respectivement entre `0.1` et `1.0` pour l’achat, et entre `-0.1` et `-1.0` pour la vente.

Chaque combinaison est évaluée sur l’année 2022, et nous retenons celle qui maximise la performance du portefeuille.

---

## Meilleur résultat obtenu (2022)

La meilleure configuration obtenue avec cette stratégie simple est :

| Paramètre                 | Valeur                          |
|---------------------------|----------------------------------|
| Modèle de sentiment       | `FinancialBERT`                 |
| Fenêtre de lissage        | 2 jour                          |
| Seuil d’achat             | `+0.7`                          |
| Seuil de vente            | `-0.4`                          |
| **Performance totale**    | **+48.64 %**                     |

---

## Courbe de capital

![Evol cour sentiment](Prix_fermeture_valeur_portefeuille.png)

L’évolution du portefeuille montre une croissance progressive corrélée au sentiment dominant.  
Malgré sa simplicité, cette approche démontre que le signal issu de Twitter contient **déjà un potentiel exploitable**.

➡️ Dans la prochaine section, nous allons concevoir un modèle **plus adaptatif**, capable de réajuster ses paramètres jour après jour.
