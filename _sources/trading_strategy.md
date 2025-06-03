# 📈 Présentation du modèle de trading adaptatif

## Introduction à l’étude

Cette section présente le **fonctionnement interne du modèle de trading adaptatif** développé dans le projet.  
L’objectif est de comprendre **comment les signaux de sentiment sont transformés en décisions d’achat ou de vente**, puis traduits en actions concrètes sur un portefeuille virtuel.

Nous allons décomposer :
- la manière dont les signaux sont construits,
- le processus d’optimisation des paramètres,
- la boucle journalière d'entraînement et d’exécution.

Un schéma explicatif illustre ce fonctionnement.

---

## ⚙️ Fonctionnement général du modèle

Le modèle repose sur l’analyse quotidienne du **sentiment extrait de Twitter** via 4 modèles différents :

- **VADER** : modèle classique de sentiment
- **FinBERT**, **DistilRoBERTa**, **DeBERTa** : modèles de langage spécialisés ou pré-entraînés sur du contenu financier ou généraliste.

Chaque jour, on cherche la **meilleure combinaison de poids** entre ces modèles pour prédire l’évolution du cours de l’action TSLA.

---

### 🔁 Boucle adaptative quotidienne

Chaque jour de trading suit les étapes suivantes :

1. **Sélection des données d'entraînement** sur les *N derniers mois*
2. **Recherche aléatoire des meilleurs paramètres** :
   - poids des modèles de sentiment
   - seuil d'achat (`buy_threshold`)
   - seuil de vente (`sell_threshold`)
   - facteur d’importance des comptes vérifiés (`weight_verified`)
3. **Sélection de la combinaison qui maximise le gain**
4. **Exécution du signal** (achat, vente ou attente)
5. **Mise à jour du portefeuille**
6. **Journalisation des décisions et performances**

---

### Paramètres optimisés chaque jour

| Paramètre             | Description                                |
|-----------------------|--------------------------------------------|
| `weights`             | Poids attribués à chaque modèle de sentiment |
| `buy_threshold`       | Seuil au-dessus duquel un achat est déclenché |
| `sell_threshold`      | Seuil en dessous duquel une vente est déclenchée |
| `weight_verified`     | Importance accordée aux tweets vérifiés     |

---

## Schéma du processus

![Process adaptatif](Process_adaptatif.svg)