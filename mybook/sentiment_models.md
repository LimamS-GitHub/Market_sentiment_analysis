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
## Schéma de l’analyse de sentiment avec Transformers

```mermaid
flowchart TD
  A[🗂 Tweet brut] --> B[🔍 Nettoyage du texte]
  B --> C[🌍 Détection de la langue]
  C --> D{Langue = Anglais ?}
  D -- Oui --> E[📤 Envoi au modèle Transformer]
  E --> F[🔎 Prédiction : POS / NEU / NEG]
  F --> G[📊 Conversion : +1 / 0 / -1]
  G --> H[📄 Enregistrement dans CSV]
  D -- Non --> X[⛔ Tweet ignoré]
  subgraph Modèles utilisés
    M1[FinBERT]
    M2[DeBERTa-v3-fin]
    M3[DistilRoBERTa-fin]
  end
  E --> M1 & M2 & M3



## Étapes d'utilisation

### 1. Prétraitement des tweets

Avant de procéder à l’analyse de sentiment, nous avons appliqué un nettoyage des tweets afin de supprimer les éléments non informatifs : liens, mentions, hashtags, ponctuation, etc.  
Nous avons également filtré les tweets par langue, en ne conservant que ceux rédigés en anglais.  
Ce choix s’explique par le fait que tous les modèles utilisés ont été entraînés sur des textes anglophones.

---

### 2. Application des modèles de sentiment

Une fois les tweets nettoyés, ils sont analysés à l’aide de modèles de type Transformer.  
Ces modèles sont accessibles via l’API `pipeline` de la bibliothèque Hugging Face.  
Pour chaque tweet, le modèle renvoie un label de sentiment : `POSITIVE`, `NEUTRAL` ou `NEGATIVE`.

Nous avons ensuite converti ces labels en valeurs numériques pour faciliter leur traitement statistique :

- `POSITIVE` → +1  
- `NEUTRAL` → 0  
- `NEGATIVE` → −1

---

### 3. Modèles utilisés

Nous avons utilisé plusieurs modèles, tous spécialisés dans le domaine financier. Cela permet d’obtenir des scores mieux adaptés au langage économique souvent employé dans les tweets.

| Modèle | Architecture | Données d’entraînement | Particularité |
|--------|--------------|------------------------|---------------|
| `ProsusAI/finbert` | BERT | Documents financiers et rapports annuels | Référence en sentiment financier |
| `deberta-v3-financial-news-sentiment` | DeBERTa-v3 | Articles de presse boursiers | Bonne compréhension du contexte |
| `distilroberta-financial-news-sentiment` | DistilRoBERTa | Actualités économiques | Modèle léger et rapide à exécuter |

Chaque modèle a été appliqué individuellement à tous les tweets, et les résultats sont enregistrés dans des colonnes distinctes (`sentiment_finbert`, `sentiment_deberta`, `sentiment_roberta`, etc.).

---

### 4. Intégration dans notre base de données

Les scores obtenus sont ajoutés directement dans notre base structurée.  
Chaque tweet est donc enrichi de plusieurs indicateurs de sentiment.  
Ce jeu de données est ensuite utilisé pour :

- construire des moyennes de sentiment par jour,
- explorer les corrélations avec les variations du cours de l'action Tesla,
- alimenter notre stratégie de trading.

---

## Pourquoi utiliser plusieurs modèles ?

Le choix d’utiliser plusieurs modèles repose sur plusieurs motivations :

- Les tweets sont souvent ambigus ou implicites. En comparant plusieurs scores, on peut repérer les divergences ou convergences d’interprétation.
- En combinant les résultats, on peut lisser les erreurs individuelles de chaque modèle.
- Cela permet également de tester l’impact de chaque modèle sur la performance globale de notre approche.

---

## Ressource pour mieux comprendre les Transformers

Pour mieux comprendre le fonctionnement des modèles Transformers et le principe de l'attention, nous recommandons la ressource suivante, particulièrement claire et interactive :

[Transformer Visualizer – Polo Club](https://poloclub.github.io/transformer-explainer/)

Ce site illustre de manière visuelle la façon dont les mots d’une phrase sont analysés et mis en relation les uns avec les autres dans un modèle Transformer.

---

Dans la section suivante, nous utiliserons ces scores pour explorer les liens entre sentiment agrégé et performance boursière.
