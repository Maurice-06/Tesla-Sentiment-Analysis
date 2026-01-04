# 🐦 Guide d'utilisation de Tweepy

Ce guide explique comment utiliser Tweepy pour collecter des tweets Tesla via l'API Twitter v2.

## 📋 Prérequis

1. **Compte développeur Twitter** avec accès à l'API v2

   - Créez un compte sur [developer.twitter.com](https://developer.twitter.com)
   - Créez une application et obtenez un **Bearer Token** (niveau Essential gratuit)

2. **Configuration du Bearer Token**

   Créez un fichier `.env` à la racine du projet :

   ```bash
   cp env.example.txt .env
   ```

   Éditez `.env` et ajoutez votre token :

   ```env
   TWITTER_BEARER_TOKEN=votre_bearer_token_ici
   ```

## 🧪 Test de connexion

Avant de collecter des tweets, testez que votre configuration fonctionne :

```bash
# Activer l'environnement virtuel
source venv_py312/bin/activate  # ou venv\Scripts\activate sur Windows

# Tester la connexion
python src/test_tweepy.py
```

Ce script va :

- ✅ Vérifier que le Bearer Token est configuré
- ✅ Tester la connexion à l'API Twitter
- ✅ Faire une recherche test de 10 tweets

### Test avec collecte d'échantillon

Pour tester la collecte complète avec un petit échantillon :

```bash
# Collecter 20 tweets de test
python src/test_tweepy.py --collect --max-tweets 20
```

## 📥 Collecte de tweets

### Méthode 1 : Script principal (collect_tesla_tweets.py)

Le script principal utilise déjà Tweepy :

```bash
python src/collect_tesla_tweets.py
```

**Fonctionnalités** :

- Collecte jusqu'à 500 tweets (configurable via variable d'environnement `MAX_TWEETS`)
- Gestion automatique des rate limits
- Sauvegarde incrémentale (évite la perte de données)
- Filtre les retweets automatiquement
- Recherche : `(Tesla OR TSLA OR @Tesla OR "Elon Musk") -is:retweet lang:en`

**Configuration** :

```bash
# Dans .env
MAX_TWEETS=500  # Nombre de tweets à collecter
```

### Méthode 2 : Utilisation directe de la classe

```python
from src.collect_tesla_tweets import TeslaTweetCollector

# Initialiser le collecteur
collector = TeslaTweetCollector()

# Tester la connexion
if collector.test_connection():
    # Collecter les tweets
    df = collector.collect_tweets(max_tweets=100)
    print(df.head())
```

## 🔍 Requêtes de recherche

Le script utilise cette requête par défaut :

```
(Tesla OR TSLA OR @Tesla OR "Elon Musk") -is:retweet lang:en
```

Vous pouvez modifier la requête dans `collect_tesla_tweets.py` ligne 60.

**Exemples de requêtes** :

- `Tesla -is:retweet lang:en` : Tweets sur Tesla en anglais
- `$TSLA -is:retweet lang:en` : Tweets avec le symbole boursier
- `Tesla Model 3 -is:retweet lang:en` : Tweets sur le Model 3
- `@Tesla -is:retweet lang:en` : Tweets mentionnant @Tesla

## ⚠️ Limitations de l'API Twitter

### Niveau Essential (Gratuit)

- **Rate limit** : 300 requêtes toutes les 15 minutes
- **Max résultats par requête** : 100 tweets
- **Période de recherche** : 7 derniers jours uniquement
- **Attente automatique** : Le script attend automatiquement si la limite est atteinte

### Calcul du temps de collecte

Pour collecter 500 tweets avec l'API Essential :

- 100 tweets par requête = 5 requêtes minimum
- 5 requêtes = ~15 minutes (si rate limit atteint)
- **Temps estimé** : 15-30 minutes selon le nombre de tweets disponibles

## 🐛 Dépannage

### Erreur : "Bearer token manquant"

**Solution** :

1. Vérifiez que le fichier `.env` existe à la racine du projet
2. Vérifiez que `TWITTER_BEARER_TOKEN` est bien défini
3. Vérifiez qu'il n'y a pas d'espaces ou de guillemets autour du token

### Erreur : "401 Unauthorized"

**Solution** :

1. Vérifiez que votre Bearer Token est valide
2. Régénérez un nouveau token sur developer.twitter.com
3. Assurez-vous que le token commence par `AAAAAA` (ou `Bearer AAAAAA`)

### Erreur : "Too Many Requests"

**Solution** :

- C'est normal ! Le script attend automatiquement 15 minutes
- Le message `wait_on_rate_limit=True` gère cela automatiquement
- Attendez que le script continue automatiquement

### Aucun tweet trouvé

**Causes possibles** :

- La requête est trop restrictive
- Pas de tweets récents correspondant (limite de 7 jours)
- Problème avec la requête de recherche

**Solution** :

- Essayez une requête plus simple : `Tesla -is:retweet lang:en`
- Vérifiez que des tweets existent sur les 7 derniers jours

## 📊 Comparaison Tweepy vs snscrape

| Caractéristique      | Tweepy (API officielle)   | snscrape              |
| -------------------- | ------------------------- | --------------------- |
| Authentification     | ✅ Requise (Bearer Token) | ❌ Non requise        |
| Rate limits          | ⚠️ Oui (300/15min)        | ✅ Aucune             |
| Période de recherche | ⚠️ 7 jours max            | ✅ Historique complet |
| Fiabilité            | ✅ Très fiable            | ⚠️ Peut être instable |
| Coût                 | ✅ Gratuit (Essential)    | ✅ Gratuit            |
| Vitesse              | ✅ Rapide                 | ⚠️ Plus lent          |

**Recommandation** :

- Utilisez **Tweepy** si vous avez un Bearer Token valide
- Utilisez **snscrape** si votre quota API est épuisé ou pour des recherches historiques

## 📚 Ressources

- [Documentation Tweepy](https://docs.tweepy.org/)
- [API Twitter v2](https://developer.twitter.com/en/docs/twitter-api)
- [Guide de recherche Twitter](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query)

## ✅ Checklist de démarrage

- [ ] Compte développeur Twitter créé
- [ ] Bearer Token obtenu
- [ ] Fichier `.env` créé avec `TWITTER_BEARER_TOKEN`
- [ ] Tweepy installé (`pip install tweepy`)
- [ ] Test de connexion réussi (`python src/test_tweepy.py`)
- [ ] Collecte de test réussie (`python src/test_tweepy.py --collect`)

Une fois tous ces points validés, vous pouvez utiliser le script principal pour collecter vos tweets !
