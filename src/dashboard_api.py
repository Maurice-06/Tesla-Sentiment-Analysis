"""
API FastAPI pour le dashboard d'analyse de sentiment Tesla
Backend moderne avec endpoints RESTful
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import sys
from typing import Optional, List, Dict
from datetime import datetime
import json
from wordcloud import WordCloud
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif pour le serveur
import matplotlib.pyplot as plt

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(
    title="Tesla Sentiment Analysis",
    description="API pour le dashboard d'analyse de sentiment Tesla",
    version="2.0.0"
)

# CORS middleware pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monter le dossier static pour servir les fichiers statiques
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_dir = os.path.join(project_root, "dashboard_static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


def load_data():
    """Charge les données d'analyse de sentiment."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    possible_files = [
        os.path.join(project_root, "data", "tesla_sentiment_results.csv"),
        os.path.join(project_root, "data", "tesla_sentiment_analysis.csv")
    ]
    
    data_file = None
    for file_path in possible_files:
        if os.path.exists(file_path):
            data_file = file_path
            break
    
    if data_file is None:
        raise FileNotFoundError(f"Aucun fichier de données trouvé. Cherché : {possible_files}")
    
    df = pd.read_csv(data_file)
    
    # Convertir la colonne date en datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Adapter les colonnes si nécessaire
    if 'polarity' not in df.columns:
        if 'sentiment_score' in df.columns:
            df['polarity'] = df['sentiment_score']
        elif 'vader_compound' in df.columns:
            df['polarity'] = df['vader_compound']
        else:
            df['polarity'] = 0.0
    
    # Créer text_cleaned si nécessaire
    if 'text_cleaned' not in df.columns and 'text' in df.columns:
        import re
        def simple_clean(text):
            if pd.isna(text):
                return ''
            text = str(text)
            text = re.sub(r'http\S+|www.\S+|https\S+', '', text, flags=re.MULTILINE)
            text = re.sub(r'@\w+', '', text)
            text = re.sub(r'#(\w+)', r'\1', text)
            text = text.lower()
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
        df['text_cleaned'] = df['text'].apply(simple_clean)
    
    return df


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Sert la page HTML du dashboard."""
    # Chemin relatif depuis le répertoire du projet
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_file = os.path.join(project_root, "dashboard_static", "index.html")
    
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    return """
    <html>
        <head><title>Tesla Sentiment Analysis</title></head>
        <body>
            <h1>Tesla Sentiment Analysis</h1>
            <p>Le fichier index.html n'a pas été trouvé dans dashboard_static/. Veuillez vérifier.</p>
        </body>
    </html>
    """


@app.get("/api/data")
async def get_data(
    sentiment: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Retourne les données filtrées."""
    try:
        df = load_data()
        
        # Appliquer les filtres
        if sentiment and sentiment != 'all':
            df = df[df['sentiment'] == sentiment]
        
        if start_date:
            df = df[df['date'].dt.date >= pd.to_datetime(start_date).date()]
        if end_date:
            df = df[df['date'].dt.date <= pd.to_datetime(end_date).date()]
        
        # Convertir en format JSON
        df['date'] = df['date'].astype(str)
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats(
    sentiment: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Retourne les statistiques agrégées."""
    try:
        df = load_data()
        
        # Appliquer les filtres
        if sentiment and sentiment != 'all':
            df = df[df['sentiment'] == sentiment]
        
        if start_date:
            df = df[df['date'].dt.date >= pd.to_datetime(start_date).date()]
        if end_date:
            df = df[df['date'].dt.date <= pd.to_datetime(end_date).date()]
        
        total = len(df)
        positive_count = len(df[df['sentiment'] == 'positive'])
        negative_count = len(df[df['sentiment'] == 'negative'])
        neutral_count = len(df[df['sentiment'] == 'neutral'])
        
        return {
            "total": total,
            "positive": {
                "count": positive_count,
                "percentage": (positive_count / total * 100) if total > 0 else 0
            },
            "negative": {
                "count": negative_count,
                "percentage": (negative_count / total * 100) if total > 0 else 0
            },
            "neutral": {
                "count": neutral_count,
                "percentage": (neutral_count / total * 100) if total > 0 else 0
            },
            "mean_polarity": float(df['polarity'].mean()) if total > 0 else 0.0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sentiment-distribution")
async def get_sentiment_distribution(
    sentiment: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Retourne la distribution des sentiments pour le graphique."""
    try:
        df = load_data()
        
        # Appliquer les filtres
        if sentiment and sentiment != 'all':
            df = df[df['sentiment'] == sentiment]
        
        if start_date:
            df = df[df['date'].dt.date >= pd.to_datetime(start_date).date()]
        if end_date:
            df = df[df['date'].dt.date <= pd.to_datetime(end_date).date()]
        
        distribution = df['sentiment'].value_counts().to_dict()
        
        return {
            "positive": distribution.get('positive', 0),
            "negative": distribution.get('negative', 0),
            "neutral": distribution.get('neutral', 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/temporal-data")
async def get_temporal_data(
    sentiment: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Retourne les données temporelles pour l'histogramme."""
    try:
        df = load_data()
        
        # Appliquer les filtres
        if sentiment and sentiment != 'all':
            df = df[df['sentiment'] == sentiment]
        
        if start_date:
            df = df[df['date'].dt.date >= pd.to_datetime(start_date).date()]
        if end_date:
            df = df[df['date'].dt.date <= pd.to_datetime(end_date).date()]
        
        df['date_only'] = df['date'].dt.date
        temporal = df.groupby('date_only').size().reset_index(name='count')
        temporal['date_only'] = temporal['date_only'].astype(str)
        
        return temporal.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/top-negative")
async def get_top_negative(n: int = 5):
    """Retourne les N tweets les plus négatifs."""
    try:
        df = load_data()
        negative_df = df[df['sentiment'] == 'negative'].copy()
        
        if len(negative_df) == 0:
            return []
        
        negative_df = negative_df.sort_values('polarity', ascending=True).head(n)
        negative_df['date'] = negative_df['date'].astype(str)
        
        return negative_df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/wordcloud")
async def get_wordcloud():
    """Génère et retourne le WordCloud des tweets négatifs en base64."""
    try:
        df = load_data()
        negative_df = df[df['sentiment'] == 'negative']
        
        if 'text_cleaned' in negative_df.columns:
            text_data = negative_df['text_cleaned'].dropna()
        elif 'text' in negative_df.columns:
            text_data = negative_df['text'].dropna()
        else:
            raise ValueError("Aucune colonne de texte disponible")
        
        if len(text_data) == 0:
            raise ValueError("Aucun tweet négatif disponible")
        
        text = ' '.join(text_data.astype(str))
        
        # Générer le WordCloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='Reds',
            max_words=100,
            relative_scaling=0.5,
            collocations=False
        ).generate(text)
        
        # Convertir en image base64
        img_buffer = BytesIO()
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        
        return {"image": f"data:image/png;base64,{img_base64}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

