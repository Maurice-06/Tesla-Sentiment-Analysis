"""
Génération de données de test réalistes pour le projet Tesla Sentiment Analysis

Ce script génère des tweets de test avec des sentiments variés pour permettre
de tester le pipeline complet sans attendre la réinitialisation du quota API.
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Tweets de test avec différents sentiments
TEST_TWEETS = [
    # Tweets positifs
    ("Tesla Model 3 is amazing! Best car I've ever owned. The autopilot feature is incredible.", "positive"),
    ("Just got my Tesla Model Y and I'm in love! The acceleration is mind-blowing. @Tesla", "positive"),
    ("TSLA stock is going to the moon! 🚀 Elon Musk is a genius. Long term hold!", "positive"),
    ("Tesla's Supercharger network is expanding rapidly. This is the future of transportation!", "positive"),
    ("My Tesla has saved me so much money on gas. Best investment ever!", "positive"),
    ("Elon Musk's vision for sustainable energy is inspiring. Tesla is changing the world!", "positive"),
    ("The Cybertruck looks incredible! Can't wait to get mine. @Tesla", "positive"),
    ("Tesla's Full Self-Driving is getting better every update. Amazing technology!", "positive"),
    ("Love my Model S! The build quality is excellent and the range is impressive.", "positive"),
    ("TSLA to $1000! The fundamentals are strong. Buy the dip!", "positive"),
    
    # Tweets négatifs
    ("Tesla quality control is terrible. My car has been in the shop 3 times this month.", "negative"),
    ("TSLA stock is crashing again. Overvalued company with production issues.", "negative"),
    ("Elon Musk's tweets are destroying Tesla's reputation. Unprofessional behavior.", "negative"),
    ("My Tesla Model 3 has so many rattles and squeaks. Build quality is poor.", "negative"),
    ("Tesla's customer service is awful. They don't respond to complaints.", "negative"),
    ("The Cybertruck is ugly and impractical. What was Elon thinking?", "negative"),
    ("TSLA is a bubble. The stock will crash when the hype dies down.", "negative"),
    ("Tesla's autopilot is dangerous. Multiple accidents reported. Not safe!", "negative"),
    ("My Tesla battery degraded 20% in one year. Not worth the money.", "negative"),
    ("Elon Musk needs to focus on production, not Twitter. Tesla is struggling.", "negative"),
    
    # Tweets neutres
    ("Tesla announced new Supercharger locations in Europe. Interesting development.", "neutral"),
    ("TSLA stock price is $250 today. Market is volatile.", "neutral"),
    ("Tesla delivered 400K vehicles this quarter. Production numbers are out.", "neutral"),
    ("Elon Musk tweeted about Tesla's new factory in Texas. Construction update.", "neutral"),
    ("Tesla Model 3 is now available in more countries. Expansion continues.", "neutral"),
    ("TSLA earnings report coming next week. Analysts are watching closely.", "neutral"),
    ("Tesla's new software update includes bug fixes. Version 11.4.2 released.", "neutral"),
    ("Tesla is hiring engineers for their new battery plant. Job openings posted.", "neutral"),
    ("Model Y production increased at Fremont factory. Manufacturing update.", "neutral"),
    ("Tesla's charging network now supports more EV models. Compatibility update.", "neutral"),
]

# Utilisateurs de test
TEST_USERS = [
    "tesla_fan_2024", "ev_enthusiast", "stock_trader", "car_lover", "tech_guru",
    "elon_follower", "investor_pro", "electric_dreams", "sustainable_life", "future_cars",
    "tesla_owner_ny", "model3_driver", "cybertruck_wait", "fsd_beta_user", "supercharger_road",
    "tsla_bull", "green_energy", "autopilot_user", "tesla_model_y", "ev_advocate"
]


def generate_test_tweets(num_tweets: int = 500) -> pd.DataFrame:
    """
    Génère des tweets de test avec des sentiments variés.
    
    Args:
        num_tweets: Nombre de tweets à générer
        
    Returns:
        DataFrame avec les tweets générés
    """
    print(f"🔧 Génération de {num_tweets} tweets de test...")
    
    tweets_data = []
    
    # Répartir les sentiments (40% positif, 30% négatif, 30% neutre)
    sentiment_distribution = {
        'positive': int(num_tweets * 0.4),
        'negative': int(num_tweets * 0.3),
        'neutral': int(num_tweets * 0.3)
    }
    
    # Générer des tweets avec variantes
    tweet_index = 0
    for sentiment, count in sentiment_distribution.items():
        for i in range(count):
            # Sélectionner un tweet de base du bon sentiment
            base_tweets = [t for t in TEST_TWEETS if t[1] == sentiment]
            if not base_tweets:
                continue
            
            base_text, _ = random.choice(base_tweets)
            
            # Ajouter des variantes pour plus de réalisme
            variants = [
                base_text,
                f"{base_text} #Tesla #TSLA",
                f"{base_text} @Tesla",
                f"Just saw: {base_text}",
                f"{base_text} What do you think?",
            ]
            text = random.choice(variants)
            
            # Générer une date aléatoire dans les 7 derniers jours
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            date = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            # Générer des métriques réalistes
            likes = random.randint(0, 1000) if sentiment == 'positive' else random.randint(0, 500)
            retweets = random.randint(0, likes // 10)
            replies = random.randint(0, likes // 20)
            quotes = random.randint(0, retweets // 5)
            
            tweet_dict = {
                'id': 1000000000000000000 + tweet_index,  # IDs Twitter-like
                'date': date,
                'text': text,
                'user': random.choice(TEST_USERS),
                'likes': likes,
                'retweets': retweets,
                'replies': replies,
                'quotes': quotes
            }
            
            tweets_data.append(tweet_dict)
            tweet_index += 1
    
    # Mélanger les tweets
    random.shuffle(tweets_data)
    
    df = pd.DataFrame(tweets_data)
    
    print(f"✅ {len(df)} tweets générés")
    print(f"   - Positifs: {len([t for t in TEST_TWEETS if t[1] == 'positive']) * (num_tweets // len(TEST_TWEETS))}")
    print(f"   - Négatifs: {len([t for t in TEST_TWEETS if t[1] == 'negative']) * (num_tweets // len(TEST_TWEETS))}")
    print(f"   - Neutres: {len([t for t in TEST_TWEETS if t[1] == 'neutral']) * (num_tweets // len(TEST_TWEETS))}")
    
    return df


def main():
    """
    Fonction principale pour générer les données de test.
    """
    output_file = "data/tesla_tweets_raw.csv"
    num_tweets = int(os.getenv('MAX_TWEETS', '500'))
    
    print("=" * 60)
    print("GÉNÉRATION DE DONNÉES DE TEST POUR TESLA SENTIMENT ANALYSIS")
    print("=" * 60)
    print("\n⚠️  Note: Ces données sont générées pour tester le pipeline.")
    print("   Pour de vraies données, utilisez l'API Twitter (après réinitialisation du quota).\n")
    
    # Générer les tweets
    df = generate_test_tweets(num_tweets)
    
    # Sauvegarder
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n💾 Données sauvegardées dans {output_file}")
    
    # Afficher un aperçu
    print("\n📊 Aperçu des données générées :")
    print(df.head(10))
    print(f"\n📈 Statistiques :")
    print(f"   Total tweets : {len(df)}")
    print(f"   Période : {df['date'].min()} à {df['date'].max()}")
    print(f"   Utilisateurs uniques : {df['user'].nunique()}")
    
    print("\n✅ Données de test prêtes !")
    print("   Vous pouvez maintenant exécuter :")
    print("   1. python src/preprocess_tesla.py")
    print("   2. python src/analyze_tesla_sentiment.py")
    print("   3. streamlit run src/tesla_dashboard.py")


if __name__ == "__main__":
    main()



