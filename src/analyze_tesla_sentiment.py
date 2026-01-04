"""
Phase 2 - NLP : Analyse de sentiment des tweets Tesla

Ce module analyse le sentiment des tweets nettoyés en utilisant VADER
(adapté aux réseaux sociaux) et TextBlob (pour comparaison).
Classification : Positif (>0.1), Négatif (<-0.1), Neutre (sinon)
"""

import pandas as pd
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk
import os
from typing import Dict, List, Tuple

# Télécharger VADER lexicon si nécessaire
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)


class TeslaSentimentAnalyzer:
    """
    Classe pour analyser le sentiment des tweets Tesla.
    
    Utilise VADER (adapté aux réseaux sociaux) et TextBlob pour comparer.
    """
    
    def __init__(self):
        """
        Initialise les analyseurs de sentiment.
        """
        # Initialiser VADER (Valence Aware Dictionary and sEntiment Reasoner)
        # VADER est spécialement conçu pour les textes des réseaux sociaux
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        print("✅ Analyseurs de sentiment initialisés (VADER + TextBlob)")
    
    def analyze_with_vader(self, text: str) -> Dict[str, float]:
        """
        Analyse le sentiment avec VADER.
        
        Args:
            text: Texte à analyser
            
        Returns:
            Dictionnaire avec les scores de polarité VADER
        """
        if pd.isna(text) or text == '':
            return {
                'compound': 0.0,
                'pos': 0.0,
                'neu': 0.0,
                'neg': 0.0
            }
        
        scores = self.vader_analyzer.polarity_scores(str(text))
        return scores
    
    def analyze_with_textblob(self, text: str) -> Dict[str, float]:
        """
        Analyse le sentiment avec TextBlob.
        
        Args:
            text: Texte à analyser
            
        Returns:
            Dictionnaire avec les scores de polarité TextBlob
        """
        if pd.isna(text) or text == '':
            return {
                'polarity': 0.0,
                'subjectivity': 0.0
            }
        
        blob = TextBlob(str(text))
        return {
            'polarity': blob.sentiment.polarity,  # Entre -1 et 1
            'subjectivity': blob.sentiment.subjectivity  # Entre 0 et 1
        }
    
    def classify_sentiment(self, polarity: float) -> str:
        """
        Classifie le sentiment selon le barème :
        - Positif : polarité > 0.1
        - Négatif : polarité < -0.1
        - Neutre : sinon
        
        Args:
            polarity: Score de polarité (généralement entre -1 et 1)
            
        Returns:
            'positive', 'negative' ou 'neutral'
        """
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str = 'text_cleaned') -> pd.DataFrame:
        """
        Analyse le sentiment pour tous les tweets du DataFrame.
        
        Args:
            df: DataFrame avec les tweets nettoyés
            text_column: Nom de la colonne contenant le texte nettoyé
            
        Returns:
            DataFrame avec les colonnes d'analyse de sentiment ajoutées
        """
        print(f"📊 Analyse de sentiment pour {len(df)} tweets...")
        
        df_analyzed = df.copy()
        
        # Analyse avec VADER
        print("   🔍 Analyse VADER en cours...")
        vader_scores = df_analyzed[text_column].apply(self.analyze_with_vader)
        
        df_analyzed['vader_compound'] = [s['compound'] for s in vader_scores]
        df_analyzed['vader_pos'] = [s['pos'] for s in vader_scores]
        df_analyzed['vader_neu'] = [s['neu'] for s in vader_scores]
        df_analyzed['vader_neg'] = [s['neg'] for s in vader_scores]
        
        # Classification avec VADER (utilise compound score)
        df_analyzed['sentiment_vader'] = df_analyzed['vader_compound'].apply(self.classify_sentiment)
        
        # Analyse avec TextBlob (pour comparaison)
        print("   🔍 Analyse TextBlob en cours...")
        textblob_scores = df_analyzed[text_column].apply(self.analyze_with_textblob)
        
        df_analyzed['textblob_polarity'] = [s['polarity'] for s in textblob_scores]
        df_analyzed['textblob_subjectivity'] = [s['subjectivity'] for s in textblob_scores]
        
        # Classification avec TextBlob
        df_analyzed['sentiment_textblob'] = df_analyzed['textblob_polarity'].apply(self.classify_sentiment)
        
        # Utiliser VADER comme classification principale (plus adapté aux réseaux sociaux)
        df_analyzed['sentiment'] = df_analyzed['sentiment_vader']
        df_analyzed['polarity'] = df_analyzed['vader_compound']
        
        print("✅ Analyse de sentiment terminée")
        
        return df_analyzed
    
    def get_top_negative_tweets(self, df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
        """
        Identifie les N tweets les plus négatifs.
        
        Args:
            df: DataFrame avec les scores de sentiment
            n: Nombre de tweets à retourner (défaut: 5)
            
        Returns:
            DataFrame avec les N tweets les plus négatifs
        """
        # Trier par polarité croissante (plus négatif en premier)
        top_negative = df.nsmallest(n, 'polarity')
        
        return top_negative[['id', 'date', 'text', 'text_cleaned', 'polarity', 
                           'sentiment', 'vader_neg', 'likes', 'retweets']]
    
    def get_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calcule les statistiques globales de sentiment.
        
        Args:
            df: DataFrame avec les scores de sentiment
            
        Returns:
            Dictionnaire avec les statistiques
        """
        total = len(df)
        
        sentiment_counts = df['sentiment'].value_counts()
        
        stats = {
            'total_tweets': total,
            'positive_count': sentiment_counts.get('positive', 0),
            'negative_count': sentiment_counts.get('negative', 0),
            'neutral_count': sentiment_counts.get('neutral', 0),
            'positive_percent': (sentiment_counts.get('positive', 0) / total) * 100,
            'negative_percent': (sentiment_counts.get('negative', 0) / total) * 100,
            'neutral_percent': (sentiment_counts.get('neutral', 0) / total) * 100,
            'mean_polarity': df['polarity'].mean(),
            'std_polarity': df['polarity'].std(),
            'mean_subjectivity': df['textblob_subjectivity'].mean()
        }
        
        return stats
    
    def detect_sarcasm_indicators(self, text: str) -> List[str]:
        """
        Détecte des indicateurs potentiels de sarcasme dans le texte.
        
        Note: Cette fonction est basique et pourrait être améliorée avec
        des modèles de deep learning fine-tunés.
        
        Args:
            text: Texte à analyser
            
        Returns:
            Liste des indicateurs détectés
        """
        if pd.isna(text) or text == '':
            return []
        
        text_lower = str(text).lower()
        indicators = []
        
        # Mots-clés souvent associés au sarcasme
        sarcasm_keywords = [
            'yeah right', 'as if', 'sure', 'obviously', 'totally',
            'great job', 'brilliant', 'perfect', 'wonderful'
        ]
        
        # Emojis sarcastiques (simplifié)
        sarcasm_patterns = [
            '🙄', '😒', '😏', '/s'  # /s est souvent utilisé pour indiquer le sarcasme
        ]
        
        for keyword in sarcasm_keywords:
            if keyword in text_lower:
                indicators.append(f"Mot-clé sarcastique: '{keyword}'")
        
        for pattern in sarcasm_patterns:
            if pattern in text:
                indicators.append(f"Pattern sarcastique: '{pattern}'")
        
        return indicators


def main():
    """
    Fonction principale pour exécuter l'analyse de sentiment.
    """
    input_file = "data/tesla_tweets_cleaned.csv"
    output_file = "data/tesla_sentiment_results.csv"
    
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(input_file):
        print(f"❌ Fichier introuvable : {input_file}")
        print("   Veuillez d'abord exécuter preprocess_tesla.py")
        return
    
    # Charger les données nettoyées
    print(f"📂 Chargement des données depuis {input_file}...")
    df_cleaned = pd.read_csv(input_file)
    print(f"   {len(df_cleaned)} tweets chargés")
    
    # Initialiser l'analyseur
    analyzer = TeslaSentimentAnalyzer()
    
    # Analyser le sentiment
    df_analyzed = analyzer.analyze_dataframe(df_cleaned)
    
    # Obtenir les statistiques
    stats = analyzer.get_statistics(df_analyzed)
    
    print("\n📈 Statistiques de sentiment :")
    print(f"   Total tweets : {stats['total_tweets']}")
    print(f"   Positifs : {stats['positive_count']} ({stats['positive_percent']:.1f}%)")
    print(f"   Négatifs : {stats['negative_count']} ({stats['negative_percent']:.1f}%)")
    print(f"   Neutres : {stats['neutral_count']} ({stats['neutral_percent']:.1f}%)")
    print(f"   Polarité moyenne : {stats['mean_polarity']:.3f}")
    
    # Identifier les 5 tweets les plus négatifs
    print("\n🔍 Identification des 5 tweets les plus négatifs...")
    top_negative = analyzer.get_top_negative_tweets(df_analyzed, n=5)
    
    print("\n📋 Top 5 tweets les plus négatifs :")
    for idx, row in top_negative.iterrows():
        print(f"\n   Tweet #{idx}:")
        print(f"   Polarité: {row['polarity']:.3f}")
        print(f"   Score négatif VADER: {row['vader_neg']:.3f}")
        print(f"   Texte: {row['text'][:150]}...")
        
        # Détecter le sarcasme
        sarcasm_indicators = analyzer.detect_sarcasm_indicators(row['text'])
        if sarcasm_indicators:
            print(f"   ⚠️  Indicateurs de sarcasme détectés: {', '.join(sarcasm_indicators)}")
    
    # Sauvegarder les résultats
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    df_analyzed.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n💾 Résultats sauvegardés dans {output_file}")


if __name__ == "__main__":
    main()

