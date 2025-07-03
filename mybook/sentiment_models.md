# 🧠 Explication des modèles de sentiment utilisés

Dans ce chapitre, nous détaillons les modèles d’analyse de sentiment utilisés pour enrichir les tweets relatifs à Tesla.  
Nous présentons d’abord **VADER**, une approche lexicale basée sur des règles, puis les **modèles Transformers** pré-entraînés adaptés au langage financier.

---

## 1. VADER : une approche lexicale basée sur des règles

**VADER** (Valence Aware Dictionary and sEntiment Reasoner) est un outil conçu pour l’analyse de sentiment dans des textes courts tels que les tweets.  
Il repose sur un **lexique de mots scorés** et un ensemble de **règles linguistiques** sans apprentissage automatique.

### Fonctionnement

Chaque mot est associé à un score de valence compris entre −4 et +4.  
Ce score peut être modulé par :

- des majuscules (`GREAT` est plus fort que `great`) ;
- des ponctuations (`!!!`) ;
- des modificateurs d’intensité (`very`, `slightly`, etc.) ;
- des négations (`not good`, `isn't bad`).

### Formule utilisée

Le score final (appelé *compound*) est normalisé dans l’intervalle [−1, +1] à l’aide de la formule :

$$\text{compound} = \frac{\sum s_i}{\sqrt{\sum s_i^2 + \alpha}}$$

Où :
- sᵢ est le score de chaque mot ou modificateur
- α est une constante (valeur par défaut : 15)

Le résultat donne un score unique reflétant la tonalité globale du tweet.

---

## 2. comprendre Les Transformers : modèles contextuels par attention

Les **Transformers** sont des modèles de langage introduits par Vaswani et al. (2017), fondés sur le mécanisme d’**attention**.  
Contrairement aux approches séquentielles (RNN, LSTM), ils traitent l’ensemble du texte en parallèle et captent les dépendances entre mots, même distants.

### Fonctionnement général

Chaque mot est converti en un vecteur, puis comparé aux autres mots du texte via des **poids d’attention**.  
Cela permet de modéliser le contexte d’un mot selon sa relation avec les autres termes.

### Modèles utilisés dans notre projet

Nous avons appliqué plusieurs Transformers spécialisés dans le domaine financier :

- `ProsusAI/finbert`
- `deberta-v3-financial-news-sentiment`
- `distilroberta-financial-news-sentiment`

Chaque tweet est analysé individuellement, et le modèle retourne une **classe de sentiment** :

- `POSITIVE` → **+1**  
- `NEUTRAL` → **0**  
- `NEGATIVE` → **−1**

Ces scores sont ensuite intégrés dans notre base de données.

---
### 🎯 Le principe de l’attention

Chaque mot dans une phrase va chercher à comprendre **à quels autres mots il doit faire attention** pour bien interpréter le sens global.  
Cela repose sur trois vecteurs :

- **Q (Query)** : ce que le mot cherche à comprendre
- **K (Key)** : les mots potentiellement utiles
- **V (Value)** : les informations que ces mots contiennent

Le poids d’attention entre deux mots est calculé par :

$$
\text{Attention}(Q_i, K_j) = \frac{Q_i \cdot K_j}{\sqrt{d_k}}
$$

où :

- \( Q_i \cdot K_j \) est le produit scalaire entre les vecteurs de requête et de clé,
- \( d_k \) est la dimension des vecteurs clés, utilisée comme facteur de normalisation.

Ensuite, une **fonction softmax** est appliquée pour convertir les scores en **poids positifs** dont la somme est égale à 1 (distribution de probabilité).

## 3. Comparaison des deux approches

| Critère                        | VADER                     | Transformers financiers         |
|-------------------------------|---------------------------|---------------------------------|
| Approche                      | Lexicale (basée sur règles) | Apprentissage profond (NLP)    |
| Données requises              | Aucune                    | Corpus pré-entraînés massifs    |
| Vitesse                       | Très rapide               | Plus lente                      |
| Capacité à comprendre le contexte | Limitée                 | Élevée                          |
| Adaptation au domaine financier| Faible                    | Excellente                      |
| Interprétabilité              | Très bonne                | Moyenne à faible                |

Nous avons utilisé VADER comme **point de référence rapide** et facilement interprétable, tandis que les Transformers ont été mobilisés pour fournir une **analyse fine**, tenant compte du langage spécifique à la finance.

---


Dans la section suivante, nous analyserons comment les scores de sentiment obtenus évoluent dans le temps et comment ils sont corrélés avec les cours boursiers de Tesla.
