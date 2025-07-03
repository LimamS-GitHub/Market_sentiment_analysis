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

Chaque jour t, le modèle suit les étapes suivantes :

1. Il sélectionne une **fenêtre historique couvrant les N derniers mois jusqu’au jour t-1**, afin de disposer d’un historique récent et pertinent.
2. Sur cette fenêtre, il applique une série de **simulations de trading**, en testant différentes combinaisons de paramètres via une **recherche aléatoire** :
   - les **poids** appliqués aux différents scores de sentiment,
   - les **seuils d’achat et de vente**,
   - la **pondération donnée aux tweets vérifiés**.
3. Pour chaque combinaison, il **simule la performance de la stratégie** sur la période considérée.
4. Il identifie la configuration ayant généré le **meilleur rendement cumulé** (ou ajusté au risque).
5. Il utilise ces **paramètres optimaux** pour produire un **signal de décision pour la journée en cours** : achat, vente ou position neutre.
6. Il exécute le trade correspondant à la **fermeture du marché**.
7. Il met à jour le portefeuille et **enregistre les performances** dans les logs.

> Cette approche permet à la stratégie de s’adapter continuellement à l'évolution du sentiment collectif et des conditions de marché, tout en intégrant un processus d’optimisation léger mais réactif.


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
