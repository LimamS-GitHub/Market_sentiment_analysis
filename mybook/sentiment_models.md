## 🤖 Comprendre les Transformers

Les modèles utilisés dans notre analyse sont basés sur l’architecture Transformer, une technologie révolutionnaire introduite en 2017 (Vaswani et al.).  
Contrairement aux RNNs ou LSTMs, ils traitent l’ensemble d’un texte en parallèle grâce à un mécanisme d’**attention**.

👉 Pour une visualisation interactive de leur fonctionnement, nous vous recommandons cette ressource :

🔗 [Transformer Visualizer (Polo Club)](https://poloclub.github.io/transformer-explainer/)

Dans notre projet, nous utilisons des versions spécialisées du Transformer, préentraînées sur des textes financiers (ex. : FinancialBERT, DeBERTa-v3-fin) pour analyser les tweets liés à Tesla.

# Explication de l'utilisation des modèles Transformers

Dans notre projet, les modèles Transformers ont été utilisés pour analyser le sentiment des tweets collectés au sujet de Tesla (TSLA).  
Chaque tweet a été passé dans un ou plusieurs modèles pré-entraînés afin d'évaluer s’il exprimait une opinion positive, neutre ou négative.

---
![Analyse de sentiment via Transformers](diagramme_transformers1.png)




---

## Ressource pour mieux comprendre les Transformers

Pour mieux comprendre le fonctionnement des modèles Transformers et le principe de l'attention, nous recommandons la ressource suivante, particulièrement claire et interactive :

[Transformer Visualizer – Polo Club](https://poloclub.github.io/transformer-explainer/)

Ce site illustre de manière visuelle la façon dont les mots d’une phrase sont analysés et mis en relation les uns avec les autres dans un modèle Transformer.

---
# Analyse des modèles de sentiment

Dans cette partie, nous revenons en détail sur les **modèles de sentiment utilisés dans notre projet**, en nous concentrant sur leur fonctionnement théorique.  
Une présentation générale des modèles (VADER, Transformers financiers, etc.) est déjà proposée dans la section précédente :  
➡️ Voir : [Collecte & Préparation des Tweets](tweet_collection.md)

Ici, nous approfondissons deux aspects essentiels :

1. Le fonctionnement lexical et mathématique de **VADER**  
2. Le principe général des **Transformers**, en lien avec leur usage pour l’analyse de sentiment

---

## 1. VADER : un modèle lexical basé sur des règles

**VADER** (Valence Aware Dictionary and sEntiment Reasoner) est un outil conçu pour détecter l’opinion exprimée dans des textes courts comme les tweets.  
Il ne repose pas sur l’apprentissage automatique, mais sur un **dictionnaire de mots pré-scorés** et un ensemble de **règles linguistiques**.

### Principes de base

Chaque mot du texte est comparé à un lexique contenant des scores allant de −4 à +4, selon leur charge émotionnelle.  
Des règles modifient ce score selon :

- les majuscules (`GOOD` est plus fort que `good`) ;
- la ponctuation (`!!` augmente l’intensité) ;
- les mots modificateurs (`very`, `kind of`, etc.) ;
- les négations (`not good` devient négatif).

### Formule utilisée

Le score final composé (entre −1 et +1) est calculé selon une formule de normalisation :

![Formule compound de VADER](formule_vader.png)
Le résultat donne un score continu, facile à interpréter.

---

## 2. Les Transformers : modèles à attention

Les modèles Transformers sont des réseaux de neurones profonds introduits par Vaswani et al. (2017).  
Ils sont devenus la base des systèmes modernes de traitement automatique du langage (NLP).

Contrairement aux approches lexicale ou séquentielle (comme RNN), les Transformers traitent tout le texte **en parallèle**, en captant les relations entre les mots grâce au mécanisme d’**attention**.

Dans notre projet, nous avons utilisé des versions préentraînées et spécialisées en finance :

- `ProsusAI/finbert`
- `deberta-v3-financial-news-sentiment`
- `distilroberta-financial-news-sentiment`

Ces modèles attribuent à chaque tweet une prédiction (`POSITIVE`, `NEUTRAL`, `NEGATIVE`), que nous avons convertie en :  
**+1**, **0** ou **−1** pour les traitements ultérieurs.

---

## 3. Comparaison VADER vs Transformers

| Critère | VADER | Transformers financiers |
|--------|-------|--------------------------|
| Approche | Lexicale (basée règles) | Apprentissage profond |
| Données requises | Aucune | Modèles pré-entraînés |
| Vitesse | Très rapide | Plus lente à l’inférence |
| Capacité contextuelle | Limitée | Élevée |
| Adaptation au langage boursier | Faible | Excellente |
| Interprétabilité | Très bonne | Moyenne |

Nous avons utilisé VADER comme point de référence simple, et les Transformers pour une analyse plus fine et spécialisée.

---

## 4. Pour aller plus loin

Pour mieux comprendre le fonctionnement des Transformers, nous recommandons cette ressource interactive :

[Visualisation interactive des Transformers (Polo Club)](https://poloclub.github.io/transformer-explainer/)

---

Dans la section suivante, nous explorerons les scores produits et leur évolution dans le temps, en lien avec le marché boursier.


---
Dans notre projet, VADER est utilisé **en parallèle** des modèles Transformers.  
Il fournit une **mesure de référence rapide**, que nous comparons aux scores plus complexes générés par FinBERT, DeBERTa, etc.

Dans la section suivante, nous utiliserons ces scores pour explorer les liens entre sentiment agrégé et performance boursière.
