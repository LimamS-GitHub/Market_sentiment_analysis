# EDA & Trading Strategy based on Twitter Sentiment (2022)

Ce notebook analyse les performances boursières de l'action Tesla (“TSLA”) en 2022 en les mettant en relation avec les sentiments extraits des tweets.

---

## 🔍 Objectifs

- Explorer la distribution des sentiments à partir de plusieurs modèles (VADER, BERT, RoBERTa, DeBERTa).
- Évaluer la valeur explicative des sentiments sur les variations de prix boursiers.
- Simuler une stratégie d'achat/vente simple basée sur le sentiment.
- Optimiser les paramètres de cette stratégie.

---

## 📁 Données utilisées

- `Data_Tesla_2022_2025.csv` : Tweets scorés par modèles de sentiment, avec dates, id, texte, vérification.
- `yfinance` : Données boursières de Tesla pour 2022 (prix d'ouverture/fermeture, volume, variation).

---

## 🧼 Etapes principales du notebook

### 1. Chargement et préparation des données
- Suppression des doublons de tweets.
- Conversion des dates, tri, filtrage sur l'année 2022.

### 2. Visualisation des distributions de sentiment
- Histograms pour chaque modèle.
- Observation : très forte proportion de scores neutres (=0).
- Hypothèse : tweets effectivement neutres, donc ignorés dans la suite de l'analyse.

### 3. Filtrage et agrégation
- Suppression des tweets avec sentiment trop proche de 0 (entre -0.1 et 0.1).
- Agrégation journalière des sentiments par groupe : comptes vérifiés / non-vérifiés.
- Moyenne pondérée des sentiments : ici, 25% vérifiés et 75% non-vérifiés.

### 4. Fusion avec données de marché
- Données TSLA via Yahoo Finance.
- Calcul des variations journalières en pourcentage.
- Fusion avec les sentiments journaliers sur la clé "date".

### 5. Normalisation
- Scores de sentiment, prix d'ouverture et variation % sont normalisés pour les comparer visuellement.

### 6. Visualisation temporelle
- Courbes colorées selon les variations de sentiment (vert/jaune/rouge).
- Superposition avec le cours normalisé de l'action TSLA.

### 7. Simulation de stratégie d'investissement
- Achat si sentiment > 0.2
- Vente si sentiment < -0.2
- Suivi du capital initial en fonction de ces décisions.
- Premier test : stratégie profitable mais modeste.

### 8. Optimisation automatique
- Grid search sur : modèle, fenêtre de lissage, seuils d'achat/vente.
- Meilleur résultat : +75.86% avec FinancialBERT, rolling=1, seuil achat=0.3, seuil vente=-0.5.

---

## ✅ Conclusion

Ce notebook montre qu'on peut tirer parti de signaux de sentiment sur Twitter pour construire une stratégie d'investissement simple et profitable, en les combinant avec une bonne agrégation temporelle et une pondération par type de compte.

Ceci constitue une première brique pour développer un modèle de trading adaptatif basé sur le sentiment social.

---

## 📌 Prochaines étapes

- Tester la robustesse sur 2023 et 2024.
- Intégrer des indicateurs techniques pour hybridation sentiment + technique.
- Raffiner le système de pondération vérifié / non-vérifié.
- Passer à une stratégie multi-actifs (Tesla + autres).

