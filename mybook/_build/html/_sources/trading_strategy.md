# 📈 Présentation du modèle de trading adaptatif

## Objectif de cette partie

Dans cette section, on présente la **logique de fonctionnement** du modèle de trading développé dans ce projet.

L’idée principale est simple :  
> Chaque jour, le modèle s’adapte aux données précédentes pour décider s’il faut acheter, vendre ou rester neutre.

On va donc expliquer :
- comment la stratégie s’ajuste dans le temps,
- quels paramètres sont recalibrés quotidiennement,
- et comment tout cela s’inscrit dans une boucle de décision automatisée.

---

## La boucle quotidienne

Chaque jour, le modèle suit les étapes suivantes :

1. Il sélectionne une **fenêtre glissante** des **N derniers mois**.
2. Sur cette fenêtre, il effectue une **recherche aléatoire de paramètres** :
   - poids appliqués aux scores de sentiment,
   - seuils d’achat et de vente,
   - pondération des tweets vérifiés.
3. Pour chaque combinaison testée, il **simule la stratégie de trading** sur la période passée.
4. Il identifie la configuration ayant obtenu le **meilleur rendement**.
5. Il utilise ces **paramètres optimaux** pour générer le **signal du jour** (achat, vente ou neutre).
6. Il exécute le trade correspondant à la fermeture du marché.
7. Il met à jour le portefeuille et **log les performances**.

> Cette approche n’est pas un entraînement au sens machine learning, mais une **optimisation adaptative basée sur backtests répétés**. Elle permet au modèle de s’ajuster chaque jour aux nouvelles dynamiques du marché.


---

## Ce que le modèle ajuste chaque jour

| Élément optimisé       | Rôle dans la décision                      |
|------------------------|--------------------------------------------|
| `weights`              | Poids appliqués aux différents scores de sentiment |
| `buy_threshold`        | Seuil au-dessus duquel un achat est déclenché |
| `sell_threshold`       | Seuil en dessous duquel une vente est déclenchée |
| `weight_verified`      | Pondération supplémentaire pour les tweets vérifiés |

---

## Schéma du processus

![Process adaptatif](Process_adaptatif.svg)

> Ce schéma résume la boucle quotidienne : entraînement, optimisation, décision, exécution — puis on passe au jour suivant.
