# 🚗 Analyse de Sentiment sur les Réseaux Sociaux - Projet Tesla

Projet académique d'analyse de sentiment sur les tweets concernant la marque Tesla, utilisant l'API Twitter, le traitement du langage naturel (NLP) et des outils de visualisation.

## 📋 Table des Matières

- [Description](#description)
- [Architecture du Projet](#architecture-du-projet)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure des Données](#structure-des-données)
- [Livrables](#livrables)

## 📝 Description

Ce projet comprend trois phases principales :

1. **Data Engineering** : Collecte et préparation des données

   - Collecte de 500 tweets récents sur Tesla via l'API Twitter v2
   - Nettoyage des données (liens, mentions, ponctuation, etc.)

2. **NLP - Analyse de Sentiment** : Traitement du langage naturel

   - Analyse de sentiment avec VADER (spécialisé réseaux sociaux) et TextBlob
   - Classification : Positif (>0.1), Négatif (<-0.1), Neutre (sinon)
   - Identification des 5 tweets les plus négatifs
   - Détection basique de sarcasme

3. **Business Intelligence** : Visualisation et Dashboard

   - Dashboard interactif Streamlit
   - Graphique camembert des sentiments
   - WordCloud des tweets négatifs
   - Histogrammes temporels
   - Analyse des tweets problématiques

   📖 **Documentation détaillée** : Voir [PHASE3_DASHBOARD.md](PHASE3_DASHBOARD.md) pour plus d'informations sur le dashboard.

## 🏗️ Architecture du Projet

```
tesla_sentiment_analysis/
│
├── data/
│   ├── tesla_tweets_raw.csv          # Tweets bruts collectés
│   ├── tesla_tweets_cleaned.csv      # Tweets nettoyés
│   └── tesla_sentiment_results.csv   # Résultats d'analyse
│
├── src/
│   ├── collect_tesla_tweets.py       # Phase 1 : Collecte Twitter
│   ├── preprocess_tesla.py           # Phase 1 : Nettoyage
│   ├── analyze_tesla_sentiment.py    # Phase 2 : Analyse NLP
│   └── tesla_dashboard.py            # Phase 3 : Dashboard Streamlit
│
├── notebooks/
│   ├── 1_collect_tweets.ipynb        # Notebook collecte
│   ├── 2_preprocess_analyze.ipynb    # Notebook nettoyage & analyse
│   └── 3_visualize_dashboard.ipynb   # Notebook visualisation
│
├── requirements.txt                  # Dépendances Python
├── .env.example                      # Exemple de configuration
├── .gitignore                        # Fichiers à ignorer
├── README.md                         # Ce fichier
└── rapport_limites.md                # Rapport d'analyse et limites
```

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Compte développeur Twitter avec accès à l'API (niveau Essential gratuit)
- Git (optionnel)

### Étapes d'installation

1. **Cloner le projet** (ou télécharger les fichiers)

```bash
git clone <url-du-repo>
cd tesla_sentiment_analysis
```

2. **Créer un environnement virtuel** (recommandé)

```bash
python -m venv venv

# Sur macOS/Linux
source venv/bin/activate

# Sur Windows
venv\Scripts\activate
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Télécharger les ressources NLTK** (automatique lors de la première exécution, ou manuellement) :

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')
```

## ⚙️ Configuration

### Configuration

#### Option A : API Twitter (Tweepy)

1. **Obtenir les credentials Twitter** :

   - Créer un compte développeur sur [developer.twitter.com](https://developer.twitter.com)
   - Créer une application et obtenir un Bearer Token (API v2 Essential)

2. **Configurer les variables d'environnement** :

Copiez `env.example.txt` vers `.env` et remplissez vos credentials :

```bash
cp env.example.txt .env
```

Éditez `.env` :

```env
# Twitter API v2 (Essential Access)
TWITTER_BEARER_TOKEN=votre_bearer_token_ici
```

#### Option B : snscrape (Alternative sans API)

**Pas de configuration nécessaire !** snscrape fonctionne sans authentification.

```bash
# Installer snscrape
pip install snscrape

# Utiliser le script alternatif
python src/collect_tesla_tweets_snscrape.py
```

**Recommandé si** :

- Votre quota API Twitter est épuisé
- Vous voulez éviter les limites de l'API
- Vous préférez une solution sans authentification

**⚠️ Important** : Ne commitez jamais le fichier `.env` ! Il est déjà dans `.gitignore`.

## 📖 Utilisation

### Méthode 1 : Exécution via scripts Python

#### Étape 1 : Collecte des tweets

**Option A : Avec l'API Twitter (Tweepy)** - Nécessite un Bearer Token

```bash
python src/collect_tesla_tweets.py
```

Ce script va :

- Se connecter à l'API Twitter
- Collecter 500 tweets récents sur Tesla
- Sauvegarder dans `data/tesla_tweets_raw.csv`

**Note** : Nécessite un Bearer Token valide et respecte les quotas de l'API.

**Option B : Avec snscrape (Recommandé si quota API épuisé)** - Sans authentification

```bash
# Installer snscrape d'abord
pip install snscrape

# Collecter les tweets
python src/collect_tesla_tweets_snscrape.py
```

Ce script va :

- Utiliser snscrape (pas de quota API)
- Collecter 500 tweets récents sur Tesla
- Sauvegarder dans `data/tesla_tweets_raw.csv`

**Avantages de snscrape** :

- ✅ Pas de quota API
- ✅ Pas d'authentification nécessaire
- ✅ Accès aux mêmes données publiques

**Note** : snscrape peut être plus lent que l'API officielle mais fonctionne sans limite.

#### Étape 2 : Nettoyage des données

```bash
python src/preprocess_tesla.py
```

Ce script va :

- Charger les tweets bruts
- Nettoyer le texte (liens, mentions, ponctuation, etc.)
- Extraire des features spécifiques à Tesla
- Sauvegarder dans `data/tesla_tweets_cleaned.csv`

#### Étape 3 : Analyse de sentiment

```bash
python src/analyze_tesla_sentiment.py
```

Ce script va :

- Analyser le sentiment avec VADER et TextBlob
- Classifier les tweets (Positif/Négatif/Neutre)
- Identifier les 5 tweets les plus négatifs
- Sauvegarder dans `data/tesla_sentiment_results.csv`

#### Étape 4 : Dashboard interactif

**🎨 Dashboard Moderne - FastAPI + Tailwind CSS**

```bash
# Rendre le script exécutable (première fois seulement)
chmod +x run_dashboard.sh

# Lancer le dashboard
./run_dashboard.sh
```

**🌐 Accès au Dashboard**

Le dashboard s'ouvrira automatiquement dans votre navigateur à :

- **URL locale** : `http://localhost:8000`
- **URL réseau** : `http://[votre-ip]:8000` (pour accès depuis d'autres appareils)

**Fonctionnalités du Dashboard :**

- 🎨 **Design épuré** : Interface moderne avec Tailwind CSS
- 📊 **Graphiques interactifs** : Chart.js pour des visualisations fluides
- ☁️ **WordCloud** : Mots les plus fréquents dans les tweets négatifs
- 📅 **Histogramme temporel** : Volume de tweets par jour
- 🔴 **Top 5 tweets négatifs** : Analyse détaillée avec design en cards
- 🔍 **Filtres interactifs** : Par sentiment et par période avec mise à jour en temps réel
- 📈 **Métriques en temps réel** : Cards avec icônes et animations
- ⚡ **Performance optimale** : API RESTful FastAPI

📖 **Documentation complète** : Voir [DASHBOARD_MODERNE.md](DASHBOARD_MODERNE.md)

**Note** : Le dashboard fonctionne avec les fichiers `tesla_sentiment_results.csv` ou `tesla_sentiment_analysis.csv` dans le dossier `data/`.

### Méthode 2 : Utilisation des notebooks Jupyter

Les notebooks fournissent une approche pédagogique étape par étape :

1. **`notebooks/1_collect_tweets.ipynb`** : Collecte des tweets
2. **`notebooks/2_preprocess_analyze.ipynb`** : Nettoyage et analyse
3. **`notebooks/3_visualize_dashboard.ipynb`** : Visualisations

Pour lancer Jupyter :

```bash
jupyter notebook
# ou
jupyter lab
```

## 📊 Structure des Données

### Fichier `tesla_tweets_raw.csv`

Colonnes :

- `id` : ID unique du tweet
- `date` : Date de publication
- `text` : Texte brut du tweet
- `user` : Nom d'utilisateur
- `likes` : Nombre de likes
- `retweets` : Nombre de retweets
- `replies` : Nombre de réponses
- `quotes` : Nombre de citations

### Fichier `tesla_tweets_cleaned.csv`

Colonnes supplémentaires :

- `text_cleaned` : Texte nettoyé
- `mentions_model` : Booléen (mention d'un modèle Tesla)
- `mentions_company` : Booléen (mention de la compagnie)
- `mentions_elon` : Booléen (mention d'Elon Musk)
- `mentioned_models` : Liste des modèles mentionnés

### Fichier `tesla_sentiment_results.csv`

Colonnes supplémentaires :

- `vader_compound` : Score compound VADER (-1 à 1)
- `vader_pos`, `vader_neu`, `vader_neg` : Scores VADER détaillés
- `textblob_polarity` : Polarité TextBlob (-1 à 1)
- `textblob_subjectivity` : Subjectivité TextBlob (0 à 1)
- `sentiment` : Classification finale (positive/negative/neutral)
- `polarity` : Score de polarité utilisé pour la classification

## 📦 Livrables

- ✅ Code Python modulaire et documenté
- ✅ 3 notebooks Jupyter pédagogiques
- ✅ Dashboard moderne interactif (FastAPI + Tailwind CSS)
- ✅ Rapport d'analyse et limites (`rapport_limites.md`)
- ✅ Documentation complète (ce README)
- ✅ **500 tweets analysés** (limite respectée avec suppression des doublons)

## 🔧 Technologies Utilisées

- **Python 3.8+**
- **Tweepy 4.14** : Interface API Twitter
- **NLTK** : Traitement du langage naturel
- **VADER** : Analyseur de sentiment pour réseaux sociaux
- **TextBlob** : Analyse de sentiment basée sur des règles
- **Pandas** : Manipulation de données
- **Matplotlib/Seaborn** : Visualisation
- **WordCloud** : Nuages de mots
- **Streamlit** : Dashboard interactif
- **Plotly** : Graphiques interactifs

## ⚠️ Limitations et Améliorations

Consultez le fichier `rapport_limites.md` pour une analyse détaillée des :

- Difficultés rencontrées avec l'API Twitter
- Limites des algorithmes VADER/TextBlob
- Problème de détection du sarcasme
- Améliorations possibles (BERT, modèles fine-tunés)
- Biais potentiels dans l'analyse

## 📄 Licence

Ce projet est réalisé dans un contexte académique.

## 👤 Auteur

Projet académique - Analyse de Sentiment sur les Réseaux Sociaux

## 🙏 Remerciements

- API Twitter pour l'accès aux données
- Communautés open-source Python pour les bibliothèques utilisées
