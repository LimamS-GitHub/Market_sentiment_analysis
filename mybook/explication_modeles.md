## 🤖 Comprendre les Transformers

Les modèles utilisés dans notre analyse sont basés sur l’architecture Transformer, une technologie révolutionnaire introduite en 2017 (Vaswani et al.).  
Contrairement aux RNNs ou LSTMs, ils traitent l’ensemble d’un texte en parallèle grâce à un mécanisme d’**attention**.

👉 Pour une visualisation interactive de leur fonctionnement, nous vous recommandons cette ressource :

🔗 [Transformer Visualizer (Polo Club)](https://poloclub.github.io/transformer-explainer/)

Dans notre projet, nous utilisons des versions spécialisées du Transformer, préentraînées sur des textes financiers (ex. : FinancialBERT, DeBERTa-v3-fin) pour analyser les tweets liés à Tesla.

# 🤖 Comment avons-nous utilisé les Transformers ?

Les Transformers ont été utilisés pour **analyser le sentiment des tweets** que nous avons collectés au sujet de Tesla ($TSLA).  
Chaque tweet nettoyé est passé dans un ou plusieurs **modèles pré-entraînés** pour déterminer s’il exprime un avis positif, neutre ou négatif.

---

## 🔄 Étapes concrètes d'utilisation

### 1. ✅ Prétraitement des tweets

Avant d’utiliser les modèles, chaque tweet est :

- **nettoyé** : suppression des liens, mentions, hashtags, emojis, ponctuation ;
- **filtré** : seuls les tweets **en anglais** sont conservés (détection automatique de langue).

Cela garantit une compatibilité optimale avec les modèles, tous entraînés sur des textes en anglais.

---

### 2. ✅ Analyse de sentiment par modèle Transformer

Chaque tweet propre est ensuite analysé avec un modèle Transformer via `transformers.pipeline` (librairie Hugging Face).  
Le modèle retourne un **label** parmi :

- `POSITIVE` → **+1**
- `NEUTRAL` → **0**
- `NEGATIVE` → **−1**

Ces scores sont utilisés pour évaluer la tonalité du tweet et construire des indicateurs de marché.

---

### 3. ✅ Modèles utilisés

| Modèle HuggingFace                             | Architecture     | Domaine entraîné                          | Utilisation principale                            |
|------------------------------------------------|------------------|--------------------------------------------|---------------------------------------------------|
| `ProsusAI/finbert`                             | BERT             | Documents financiers (10-K, actualités)   | Référence pour le sentiment boursier              |
| `Yiyang/deberta-v3-financial-news-sentiment`   | DeBERTa-v3       | News économiques et financières           | Meilleure compréhension contextuelle              |
| `NbAiLab/distilroberta-financial-news-sentiment` | DistilRoBERTa | Articles de presse spécialisés finance    | Léger, rapide à l’inférence                       |

Chaque modèle attribue un score stocké dans une colonne distincte (`sentiment_finbert`, `sentiment_deberta`, `sentiment_roberta`).

---

### 4. ✅ Structuration des résultats

Ces scores sont ajoutés directement dans notre base de données finale (`tweets_with_sentiment.csv`) :

- Chaque ligne = 1 tweet + 3 scores de sentiment
- Permet ensuite une **agrégation journalière** et des calculs statistiques
- Sert de base à la construction des signaux dans la stratégie de trading

---

## 🎯 Pourquoi utiliser plusieurs modèles ?

Cela nous permet de :

- **Comparer les interprétations** de tweets parfois ambigus ;
- **Combiner plusieurs sources** pour lisser le bruit et améliorer la robustesse ;
- **Tester les performances de chaque modèle** dans notre pipeline de trading.

---

## 🔗 Pour mieux comprendre l’architecture Transformer

Nous recommandons cette visualisation interactive :

👉 [Transformer Visualizer – Polo Club](https://poloclub.github.io/transformer-explainer/)

Elle montre comment les modèles attribuent de l’importance à chaque mot dans une phrase grâce au mécanisme d’**attention**, cœur du fonctionnement des Transformers.

---

➡️ Partie suivante : [Analyse exploratoire du sentiment](analyse_sentiment.html)
