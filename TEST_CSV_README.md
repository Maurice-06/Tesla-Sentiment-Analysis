# 🧪 Guide de Test avec les Fichiers CSV

Ce guide explique comment tester et utiliser les fichiers CSV existants pour l'analyse de sentiment sur les tweets Tesla.

## 📁 Fichiers CSV Disponibles

### 1. `data/tesla_tweets_raw.csv`

- **Contenu** : 500 tweets bruts sur Tesla
- **Colonnes** :
  - `id` : Identifiant unique du tweet
  - `date` : Date de publication
  - `text` : Texte du tweet
  - `user` : Nom d'utilisateur
  - `likes` : Nombre de likes
  - `retweets` : Nombre de retweets
  - `replies` : Nombre de réponses
  - `quotes` : Nombre de citations

### 2. `data/tesla_sentiment_analysis.csv`

- **Contenu** : 600 tweets analysés avec scores de sentiment
- **Colonnes supplémentaires** :
  - `sentiment` : Classification (positive/negative/neutral)
  - `sentiment_score` : Score compound VADER (-1 à 1)
  - `textblob_polarity` : Polarité TextBlob (-1 à 1)
  - `textblob_subjectivity` : Subjectivité TextBlob (0 à 1)
  - `vader_pos`, `vader_neu`, `vader_neg` : Scores VADER détaillés
  - `vader_compound` : Score compound VADER

## 🚀 Tests Rapides

### Test Simple (Recommandé)

Le script le plus simple pour tester rapidement :

```bash
python3 src/test_csv_simple.py
```

**Résultat attendu** :

- ✅ Affichage du nombre de tweets dans chaque fichier
- ✅ Distribution des sentiments
- ✅ Statistiques sur les scores
- ✅ Top tweets positifs et négatifs

### Test Complet (avec graphiques)

Pour une analyse plus détaillée avec visualisations :

```bash
python3 src/test_with_csv.py
```

**Options disponibles** :

```bash
# Analyser uniquement les données brutes
python3 src/test_with_csv.py --raw-only

# Analyser uniquement les données de sentiment
python3 src/test_with_csv.py --sentiment-only

# Spécifier un autre répertoire
python3 src/test_with_csv.py --data-dir data
```

**Fonctionnalités** :

- 📊 Statistiques descriptives complètes
- 📈 Graphiques (distribution, histogrammes, comparaisons)
- 🔍 Analyse détaillée des utilisateurs
- 📅 Analyse temporelle

## 📊 Résultats Attendus

### Distribution des Sentiments

D'après les données actuelles :

- **Positifs** : ~39% (233 tweets)
- **Neutres** : ~35% (210 tweets)
- **Négatifs** : ~26% (157 tweets)

### Scores de Sentiment

- **Moyenne** : ~0.117 (légèrement positif)
- **Médiane** : 0.000 (neutre)
- **Min** : -0.796 (très négatif)
- **Max** : 0.910 (très positif)

## 💡 Utilisation dans votre Code

### Charger les données

```python
import pandas as pd

# Charger les tweets bruts
df_raw = pd.read_csv('data/tesla_tweets_raw.csv')
print(f"Tweets chargés: {len(df_raw)}")

# Charger les tweets analysés
df_sentiment = pd.read_csv('data/tesla_sentiment_analysis.csv')
print(f"Tweets analysés: {len(df_sentiment)}")
```

### Analyser les sentiments

```python
# Distribution des sentiments
sentiment_counts = df_sentiment['sentiment'].value_counts()
print(sentiment_counts)

# Score moyen
mean_score = df_sentiment['sentiment_score'].mean()
print(f"Score moyen: {mean_score:.3f}")

# Top tweets positifs
top_positive = df_sentiment.nlargest(5, 'sentiment_score')
print(top_positive[['text', 'sentiment_score', 'user']])
```

### Filtrer par sentiment

```python
# Tweets positifs uniquement
positive_tweets = df_sentiment[df_sentiment['sentiment'] == 'positive']
print(f"Tweets positifs: {len(positive_tweets)}")

# Tweets très négatifs (score < -0.5)
very_negative = df_sentiment[df_sentiment['sentiment_score'] < -0.5]
print(f"Tweets très négatifs: {len(very_negative)}")
```

## 🔄 Collecte de Nouveaux Tweets avec Tweepy

Si vous voulez collecter de nouveaux tweets similaires à ceux du CSV :

```bash
# Test de connexion Tweepy
python3 src/test_tweepy.py

# Collecte de nouveaux tweets (nécessite Bearer Token)
python3 src/collect_tesla_tweets.py
```

Voir le guide `GUIDE_TWEEPY.md` pour plus de détails.

## 📈 Prochaines Étapes

1. **Analyser les données existantes** :

   ```bash
   python3 src/test_csv_simple.py
   ```

2. **Explorer avec pandas** :

   - Ouvrir les CSV dans un notebook Jupyter
   - Créer vos propres visualisations
   - Analyser des patterns spécifiques

3. **Comparer avec de nouvelles données** :
   - Collecter de nouveaux tweets avec Tweepy
   - Comparer les distributions de sentiment
   - Analyser l'évolution dans le temps

## ⚠️ Notes Importantes

- Les fichiers CSV contiennent des données d'exemple/test
- Les IDs des tweets sont fictifs (pour des raisons de confidentialité)
- Les dates sont dans une plage récente pour les tests
- Pour des données réelles, utilisez Tweepy avec un Bearer Token valide

## 🐛 Dépannage

### Erreur : "FileNotFoundError"

**Solution** : Vérifiez que vous êtes dans le répertoire racine du projet :

```bash
cd /chemin/vers/tesla_sentiment_analysis
```

### Erreur : "ModuleNotFoundError"

**Solution** : Installez les dépendances :

```bash
pip install pandas
```

### Les graphiques ne s'affichent pas

**Solution** : Le script `test_with_csv.py` sauvegarde les graphiques dans `data/` plutôt que de les afficher. Vérifiez le dossier `data/` pour les fichiers PNG.

## ✅ Checklist de Test

- [ ] Les fichiers CSV existent dans `data/`
- [ ] Le script `test_csv_simple.py` s'exécute sans erreur
- [ ] Les statistiques sont cohérentes
- [ ] Les tweets sont bien formatés
- [ ] Les scores de sentiment sont dans la plage [-1, 1]

Une fois ces tests validés, vous pouvez utiliser les données CSV pour vos analyses !
