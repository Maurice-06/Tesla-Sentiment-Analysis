"""
Phase 1 - Data Engineering : Prétraitement et nettoyage des tweets Tesla

Ce module nettoie les tweets collectés en supprimant :
- Les liens HTTP/HTTPS
- Les mentions @user
- La ponctuation et les chiffres
- Convertit en minuscules
- Supprime les stopwords
- Optionnellement : lemmatisation
"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from typing import List, Set
import os

# Télécharger les ressources NLTK nécessaires (si pas déjà fait)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)


class TeslaTextPreprocessor:
    """
    Classe pour nettoyer et prétraiter les tweets sur Tesla.
    
    Effectue un nettoyage complet du texte pour préparer l'analyse
    de sentiment.
    """
    
    def __init__(self, language: str = 'english', lemmatize: bool = False):
        """
        Initialise le preprocessor.
        
        Args:
            language: Langue pour les stopwords ('english' ou 'french')
            lemmatize: Si True, applique la lemmatisation
        """
        self.language = language
        self.lemmatize = lemmatize
        
        # Charger les stopwords
        self.stop_words = set(stopwords.words(language))
        # Ajouter aussi les stopwords français si anglais
        if language == 'english':
            try:
                french_stopwords = set(stopwords.words('french'))
                self.stop_words = self.stop_words.union(french_stopwords)
            except:
                pass
        
        # Initialiser le lemmatiseur si nécessaire
        if lemmatize:
            self.lemmatizer = WordNetLemmatizer()
        else:
            self.lemmatizer = None
        
        # Mots-clés spécifiques à Tesla pour l'extraction de features
        self.tesla_keywords = {
            'models': ['model 3', 'model y', 'model s', 'model x', 'cybertruck', 
                      'semi', 'roadster'],
            'company': ['tesla', 'tsla'],
            'people': ['elon', 'musk', 'elon musk']
        }
    
    def clean_tweet(self, text: str) -> str:
        """
        Nettoie un tweet en supprimant liens, mentions, ponctuation, etc.
        
        Args:
            text: Texte brut du tweet
            
        Returns:
            Texte nettoyé
        """
        if pd.isna(text) or text == '':
            return ''
        
        # Convertir en string
        text = str(text)
        
        # 1. Supprimer les liens HTTP/HTTPS
        text = re.sub(r'http\S+|www.\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # 2. Supprimer les mentions @user
        text = re.sub(r'@\w+', '', text)
        
        # 3. Supprimer les hashtags (garder le mot sans #)
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # 4. Supprimer les caractères spéciaux et ponctuation (garder lettres et espaces)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # 5. Supprimer les chiffres
        text = re.sub(r'\d+', '', text)
        
        # 6. Convertir en minuscules
        text = text.lower()
        
        # 7. Supprimer les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        # 8. Tokeniser et supprimer les stopwords
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in self.stop_words]
        
        # 9. Supprimer les tokens trop courts (moins de 2 caractères)
        tokens = [token for token in tokens if len(token) > 2]
        
        # 10. Lemmatisation (optionnelle)
        if self.lemmatize and self.lemmatizer:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        # Rejoindre les tokens en texte
        cleaned_text = ' '.join(tokens)
        
        # Supprimer les espaces en début/fin
        cleaned_text = cleaned_text.strip()
        
        return cleaned_text
    
    def extract_tesla_features(self, text: str) -> dict:
        """
        Extrait des features spécifiques à Tesla depuis le texte.
        
        Args:
            text: Texte du tweet (original ou nettoyé)
            
        Returns:
            Dictionnaire avec les features extraites
        """
        if pd.isna(text) or text == '':
            return {
                'mentions_model': False,
                'mentions_company': False,
                'mentions_elon': False,
                'mentioned_models': []
            }
        
        text_lower = str(text).lower()
        
        features = {
            'mentions_model': False,
            'mentions_company': False,
            'mentions_elon': False,
            'mentioned_models': []
        }
        
        # Vérifier la mention de modèles
        for model in self.tesla_keywords['models']:
            if model in text_lower:
                features['mentions_model'] = True
                features['mentioned_models'].append(model)
        
        # Vérifier la mention de la compagnie
        for keyword in self.tesla_keywords['company']:
            if keyword in text_lower:
                features['mentions_company'] = True
                break
        
        # Vérifier la mention d'Elon Musk
        for keyword in self.tesla_keywords['people']:
            if keyword in text_lower:
                features['mentions_elon'] = True
                break
        
        return features
    
    def preprocess_dataframe(
        self, 
        df: pd.DataFrame,
        text_column: str = 'text'
    ) -> pd.DataFrame:
        """
        Prétraite un DataFrame complet de tweets.
        
        Args:
            df: DataFrame avec les tweets bruts
            text_column: Nom de la colonne contenant le texte
            
        Returns:
            DataFrame avec les colonnes nettoyées
        """
        print(f"🧹 Nettoyage de {len(df)} tweets...")
        
        # Créer une copie pour ne pas modifier l'original
        df_cleaned = df.copy()
        
        # Nettoyer les tweets
        df_cleaned['text_cleaned'] = df_cleaned[text_column].apply(self.clean_tweet)
        
        # Extraire les features Tesla
        print("🔍 Extraction des features Tesla...")
        features_list = df_cleaned[text_column].apply(self.extract_tesla_features)
        
        # Ajouter les features au DataFrame
        df_cleaned['mentions_model'] = [f['mentions_model'] for f in features_list]
        df_cleaned['mentions_company'] = [f['mentions_company'] for f in features_list]
        df_cleaned['mentions_elon'] = [f['mentions_elon'] for f in features_list]
        df_cleaned['mentioned_models'] = [f['mentioned_models'] for f in features_list]
        
        # Supprimer les tweets vides après nettoyage
        initial_count = len(df_cleaned)
        df_cleaned = df_cleaned[df_cleaned['text_cleaned'].str.len() > 0]
        removed_count = initial_count - len(df_cleaned)
        
        if removed_count > 0:
            print(f"⚠️  {removed_count} tweets vides supprimés après nettoyage")
        
        print(f"✅ Nettoyage terminé : {len(df_cleaned)} tweets valides")
        
        return df_cleaned


def main():
    """
    Fonction principale pour exécuter le prétraitement.
    """
    input_file = "data/tesla_tweets_raw.csv"
    output_file = "data/tesla_tweets_cleaned.csv"
    
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(input_file):
        print(f"❌ Fichier introuvable : {input_file}")
        print("   Veuillez d'abord exécuter collect_tesla_tweets.py")
        return
    
    # Charger les données brutes
    print(f"📂 Chargement des données depuis {input_file}...")
    df_raw = pd.read_csv(input_file)
    print(f"   {len(df_raw)} tweets chargés")
    
    # Initialiser le preprocessor
    preprocessor = TeslaTextPreprocessor(language='english', lemmatize=False)
    
    # Nettoyer les données
    df_cleaned = preprocessor.preprocess_dataframe(df_raw)
    
    # Sauvegarder
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    df_cleaned.to_csv(output_file, index=False, encoding='utf-8')
    print(f"💾 Données nettoyées sauvegardées dans {output_file}")
    
    # Afficher un aperçu
    print("\n📊 Aperçu des données nettoyées :")
    print(df_cleaned[['text', 'text_cleaned', 'mentions_model', 'mentions_elon']].head(3))
    
    # Statistiques
    print(f"\n📈 Statistiques de nettoyage :")
    print(f"   Tweets mentionnant un modèle : {df_cleaned['mentions_model'].sum()}")
    print(f"   Tweets mentionnant Elon : {df_cleaned['mentions_elon'].sum()}")
    print(f"   Longueur moyenne du texte nettoyé : {df_cleaned['text_cleaned'].str.len().mean():.1f} caractères")


if __name__ == "__main__":
    main()

