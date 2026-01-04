"""
Phase 1 - Data Engineering : Collecte de tweets Tesla avec Tweepy

Ce module collecte les tweets récents concernant Tesla depuis l'API Twitter v2.
Il gère les rate limits, filtre les retweets et sauvegarde les données brutes.
"""

import os
import sys

# Workaround pour imghdr supprimé dans Python 3.13+
if sys.version_info >= (3, 13):
    import importlib.util
    spec = importlib.util.spec_from_file_location("imghdr", os.path.join(os.path.dirname(__file__), "imghdr_compat.py"))
    imghdr = importlib.util.module_from_spec(spec)
    sys.modules["imghdr"] = imghdr
    spec.loader.exec_module(imghdr)

import tweepy
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Optional
import time

# Charger les variables d'environnement
load_dotenv()


class TeslaTweetCollector:
    """
    Classe pour collecter des tweets sur Tesla via l'API Twitter.
    
    Gère l'authentification, la collecte avec pagination, et la sauvegarde
    des données en CSV.
    """
    
    def __init__(self, bearer_token: Optional[str] = None):
        """
        Initialise le collecteur avec les credentials Twitter.
        
        Args:
            bearer_token: Token Bearer pour l'API v2 (ou depuis .env)
        """
        self.bearer_token = bearer_token or os.getenv('TWITTER_BEARER_TOKEN')
        
        if not self.bearer_token:
            raise ValueError(
                "Bearer token manquant. Définissez TWITTER_BEARER_TOKEN dans .env"
            )
        
        # Initialiser le client Tweepy avec gestion des rate limits
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            wait_on_rate_limit=True  # Attendre automatiquement si limite atteinte
        )
        
        # Requête de recherche pour Tesla
        # Recherche : Tesla, TSLA, @Tesla, Elon Musk (exclut les retweets)
        self.query = "(Tesla OR TSLA OR @Tesla OR \"Elon Musk\") -is:retweet lang:en"
    
    def _save_incremental(self, tweets_data: List[Dict], output_file: str, existing_ids: set):
        """
        Sauvegarde incrémentale des tweets pour éviter la perte de données.
        """
        if not tweets_data:
            return
        
        df_new = pd.DataFrame(tweets_data)
        
        # Charger les données existantes ou créer un nouveau DataFrame
        if os.path.exists(output_file):
            try:
                df_existing = pd.read_csv(output_file)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                # Supprimer les doublons basés sur l'ID
                df_combined = df_combined.drop_duplicates(subset=['id'], keep='last')
            except:
                df_combined = df_new
        else:
            df_combined = df_new
        
        # Sauvegarder
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        df_combined.to_csv(output_file, index=False, encoding='utf-8')
        
    def collect_tweets(
        self, 
        max_tweets: int = 500,
        output_file: str = "data/tesla_tweets_raw.csv"
    ) -> pd.DataFrame:
        """
        Collecte les tweets récents sur Tesla.
        
        Args:
            max_tweets: Nombre maximum de tweets à collecter (défaut: 500)
            output_file: Chemin du fichier CSV de sortie
            
        Returns:
            DataFrame pandas contenant les tweets collectés
        """
        print(f"🔍 Collecte de {max_tweets} tweets sur Tesla...")
        print(f"⏳ Note: Avec l'API Essential, cela peut prendre plusieurs cycles de rate limit (15 min chacun)")
        print(f"   Le script attendra automatiquement et continuera jusqu'à atteindre {max_tweets} tweets.\n")
        
        tweets_data = []
        tweet_count = 0
        
        # Charger les tweets existants si le fichier existe déjà
        if os.path.exists(output_file):
            try:
                existing_df = pd.read_csv(output_file)
                tweet_count = len(existing_df)
                print(f"📂 {tweet_count} tweets déjà collectés, reprise de la collecte...")
                # Charger les IDs existants pour éviter les doublons
                existing_ids = set(existing_df['id'].astype(str))
            except:
                existing_ids = set()
        else:
            existing_ids = set()
        
        try:
            # Utiliser search_recent_tweets pour l'API v2 (gratuite Essential)
            # max_results par requête limité à 100 (maximum autorisé)
            for tweet in tweepy.Paginator(
                self.client.search_recent_tweets,
                query=self.query,
                tweet_fields=['created_at', 'public_metrics', 'author_id', 'text'],
                user_fields=['username', 'name'],
                expansions=['author_id'],
                max_results=100,  # Maximum par requête
                limit=((max_tweets // 100) + 1)  # Nombre de pages nécessaires
            ).flatten(limit=max_tweets):
                
                # Éviter les doublons
                tweet_id_str = str(tweet.id)
                if tweet_id_str in existing_ids:
                    continue
                
                # Extraire les métriques publiques
                metrics = tweet.public_metrics
                
                # Créer un dictionnaire avec les données du tweet
                tweet_dict = {
                    'id': tweet.id,
                    'date': tweet.created_at,
                    'text': tweet.text,
                    'user_id': tweet.author_id,
                    'likes': metrics.get('like_count', 0),
                    'retweets': metrics.get('retweet_count', 0),
                    'replies': metrics.get('reply_count', 0),
                    'quotes': metrics.get('quote_count', 0)
                }
                
                tweets_data.append(tweet_dict)
                existing_ids.add(tweet_id_str)
                tweet_count += 1
                
                # Sauvegarder périodiquement (tous les 10 tweets)
                if len(tweets_data) >= 10:
                    self._save_incremental(tweets_data, output_file, existing_ids)
                    tweets_data = []  # Réinitialiser après sauvegarde
                
                # Afficher la progression tous les 10 tweets
                if tweet_count % 10 == 0:
                    print(f"   ✅ {tweet_count}/{max_tweets} tweets collectés ({tweet_count*100//max_tweets}%)...")
                
                # Arrêter si on a atteint le maximum
                if tweet_count >= max_tweets:
                    break
            
            # Sauvegarder les tweets restants
            if tweets_data:
                self._save_incremental(tweets_data, output_file, existing_ids)
            
            print(f"✅ Collecte terminée : {tweet_count} tweets collectés")
            
        except tweepy.TooManyRequests:
            print("❌ Erreur : Trop de requêtes. Attente automatique...")
            time.sleep(60)
            return self.collect_tweets(max_tweets, output_file)
            
        except tweepy.Unauthorized:
            raise ValueError("❌ Erreur d'authentification. Vérifiez votre bearer token.")
            
        except tweepy.BadRequest as e:
            raise ValueError(f"❌ Requête invalide : {e}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la collecte : {e}")
            raise
        
        # Créer le DataFrame
        df = pd.DataFrame(tweets_data)
        
        # Récupérer les usernames (nécessite une requête supplémentaire)
        if len(df) > 0 and 'user_id' in df.columns:
            try:
                user_ids = df['user_id'].unique().tolist()
                users = self.client.get_users(ids=user_ids, user_fields=['username', 'name'])
                
                # Créer un mapping user_id -> username
                if users.data:
                    user_map = {user.id: user.username for user in users.data}
                    df['user'] = df['user_id'].map(user_map).fillna('unknown')
                else:
                    df['user'] = 'unknown'
                
            except Exception as e:
                print(f"⚠️  Impossible de récupérer les usernames : {e}")
                df['user'] = 'unknown'
        
        # Réorganiser les colonnes pour la sortie
        columns_order = ['id', 'date', 'text', 'user', 'likes', 'retweets', 'replies', 'quotes']
        df = df[[col for col in columns_order if col in df.columns]]
        
        # S'assurer qu'on a exactement max_tweets (500) et supprimer les doublons par ID
        df = df.drop_duplicates(subset=['id'], keep='first')
        
        # Limiter à max_tweets si on en a plus
        if len(df) > max_tweets:
            print(f"⚠️  {len(df)} tweets collectés, limitation à {max_tweets} tweets")
            df = df.head(max_tweets)
        
        # Sauvegarder en CSV
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"💾 {len(df)} tweets uniques sauvegardés dans {output_file} (limite: {max_tweets})")
        
        return df
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à l'API Twitter.
        
        Returns:
            True si la connexion fonctionne, False sinon
        """
        try:
            # Faire une requête test pour vérifier l'authentification
            test_query = "Tesla -is:retweet lang:en"
            response = self.client.search_recent_tweets(
                query=test_query,
                max_results=10
            )
            print("✅ Connexion à l'API Twitter réussie")
            return True
            
        except tweepy.Unauthorized as e:
            print(f"❌ Erreur d'authentification (401 Unauthorized)")
            print(f"   Le Bearer Token est invalide, expiré ou mal configuré.")
            print(f"   Vérifiez votre fichier .env et assurez-vous que :")
            print(f"   1. TWITTER_BEARER_TOKEN contient un token valide")
            print(f"   2. Le token commence par 'AAAAAA' ou 'Bearer AAAAAA'")
            print(f"   3. Le token n'est pas expiré (générez-en un nouveau si nécessaire)")
            print(f"   4. Pas d'espaces ou guillemets autour du token dans .env")
            return False
        except Exception as e:
            print(f"❌ Erreur de connexion : {e}")
            return False


def main():
    """
    Fonction principale pour exécuter la collecte.
    """
    try:
        # Initialiser le collecteur
        collector = TeslaTweetCollector()
        
        # Tester la connexion
        if not collector.test_connection():
            print("❌ Impossible de se connecter à l'API Twitter")
            return
        
        # Collecter 500 tweets (ou moins pour un test rapide)
        # Pour un test rapide, utilisez max_tweets=100
        max_tweets = int(os.getenv('MAX_TWEETS', '500'))
        df_tweets = collector.collect_tweets(max_tweets=max_tweets)
        
        # Afficher un aperçu
        print("\n📊 Aperçu des données collectées :")
        print(df_tweets.head())
        print(f"\n📈 Statistiques :")
        print(f"   Total tweets : {len(df_tweets)}")
        print(f"   Période : {df_tweets['date'].min()} à {df_tweets['date'].max()}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution : {e}")
        raise


if __name__ == "__main__":
    main()

