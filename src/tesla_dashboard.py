"""
Phase 3 - Business Intelligence : Dashboard interactif Streamlit

Ce module crée un dashboard interactif pour visualiser l'analyse de sentiment
des tweets Tesla avec :
- Camembert des sentiments
- WordCloud des tweets négatifs
- Histogramme temporel
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
import os
import sys

# Ajouter le répertoire parent au path pour importer les modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from analyze_tesla_sentiment import TeslaSentimentAnalyzer

# Chemin vers le logo Tesla
tesla_logo_path = os.path.join(project_root, "tesla_logo.png")

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Tesla Sentiment Analysis",
    page_icon=tesla_logo_path if os.path.exists(tesla_logo_path) else "🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design professionnel
st.markdown("""
<style>
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    @keyframes glow {
        0%, 100% {
            filter: drop-shadow(0 0 8px rgba(227, 25, 55, 0.6)) drop-shadow(0 0 16px rgba(227, 25, 55, 0.4));
        }
        50% {
            filter: drop-shadow(0 0 12px rgba(227, 25, 55, 0.8)) drop-shadow(0 0 24px rgba(227, 25, 55, 0.6)) drop-shadow(0 0 32px rgba(227, 25, 55, 0.4));
        }
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-50px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #E31937, #FF6B6B, #FF8E8E, #FF6B6B, #E31937);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInDown 1s ease-out, gradientShift 4s ease infinite, glow 3s ease-in-out infinite;
        letter-spacing: 3px;
        padding: 1.5rem;
        position: relative;
        text-transform: uppercase;
        transition: transform 0.3s ease;
    }
    
    .main-header:hover {
        transform: scale(1.05);
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #E31937;
    }
    .stPlotlyChart {
        background-color: white;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def load_data():
    """
    Charge les données d'analyse de sentiment.
    
    Returns:
        DataFrame avec les données analysées ou None si erreur
    """
    # Essayer plusieurs fichiers possibles
    possible_files = [
        "data/tesla_sentiment_results.csv",
        "data/tesla_sentiment_analysis.csv"
    ]
    
    data_file = None
    for file_path in possible_files:
        if os.path.exists(file_path):
            data_file = file_path
            break
    
    if data_file is None:
        st.error(f"❌ Fichier de données introuvable. Cherché : {', '.join(possible_files)}")
        st.info("💡 Veuillez d'abord exécuter le pipeline complet :")
        st.code("""
1. python src/collect_tesla_tweets.py
2. python src/preprocess_tesla.py
3. python src/analyze_tesla_sentiment.py
        """)
        return None
    
    try:
        df = pd.read_csv(data_file)
        
        # Convertir la colonne date en datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Adapter les colonnes si nécessaire pour compatibilité
        # Si 'polarity' n'existe pas, utiliser 'sentiment_score' ou 'vader_compound'
        if 'polarity' not in df.columns:
            if 'sentiment_score' in df.columns:
                df['polarity'] = df['sentiment_score']
            elif 'vader_compound' in df.columns:
                df['polarity'] = df['vader_compound']
            else:
                st.warning("⚠️ Colonne 'polarity' introuvable. Certaines fonctionnalités peuvent être limitées.")
                df['polarity'] = 0.0
        
        # Si 'text_cleaned' n'existe pas, créer une version simplifiée depuis 'text'
        if 'text_cleaned' not in df.columns and 'text' in df.columns:
            import re
            def simple_clean(text):
                if pd.isna(text):
                    return ''
                text = str(text)
                # Supprimer les liens
                text = re.sub(r'http\S+|www.\S+|https\S+', '', text, flags=re.MULTILINE)
                # Supprimer les mentions
                text = re.sub(r'@\w+', '', text)
                # Supprimer les hashtags (garder le mot)
                text = re.sub(r'#(\w+)', r'\1', text)
                # Convertir en minuscules
                text = text.lower()
                # Supprimer les espaces multiples
                text = re.sub(r'\s+', ' ', text)
                return text.strip()
            df['text_cleaned'] = df['text'].apply(simple_clean)
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {e}")
        return None


def create_sentiment_pie_chart(df: pd.DataFrame):
    """
    Crée un graphique camembert pour la distribution des sentiments.
    
    Args:
        df: DataFrame avec les données analysées
        
    Returns:
        Figure Plotly
    """
    sentiment_counts = df['sentiment'].value_counts()
    
    # Définir les couleurs selon le sentiment
    colors = {
        'positive': '#2E7D32',  # Vert
        'negative': '#C62828',  # Rouge
        'neutral': '#757575'    # Gris
    }
    
    color_list = [colors.get(sent, '#757575') for sent in sentiment_counts.index]
    
    fig = go.Figure(data=[go.Pie(
        labels=sentiment_counts.index.str.title(),
        values=sentiment_counts.values,
        hole=0.4,  # Donut chart
        marker_colors=color_list,
        textinfo='label+percent',
        textfont_size=14,
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': 'Distribution des Sentiments',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        showlegend=True,
        height=500
    )
    
    return fig


def create_wordcloud_negative(df: pd.DataFrame):
    """
    Crée un WordCloud des mots les plus fréquents dans les tweets négatifs.
    
    Args:
        df: DataFrame avec les données analysées
        
    Returns:
        Figure Matplotlib
    """
    # Filtrer les tweets négatifs
    negative_df = df[df['sentiment'] == 'negative']
    
    # Utiliser text_cleaned si disponible, sinon text
    if 'text_cleaned' in negative_df.columns:
        negative_tweets = negative_df['text_cleaned'].dropna()
    elif 'text' in negative_df.columns:
        negative_tweets = negative_df['text'].dropna()
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Aucune colonne de texte disponible', 
               ha='center', va='center', fontsize=16)
        ax.axis('off')
        return fig
    
    if len(negative_tweets) == 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Aucun tweet négatif disponible', 
               ha='center', va='center', fontsize=16)
        ax.axis('off')
        return fig
    
    # Combiner tous les tweets négatifs
    text = ' '.join(negative_tweets.astype(str))
    
    # Créer le WordCloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='Reds',
        max_words=100,
        relative_scaling=0.5,
        collocations=False
    ).generate(text)
    
    # Créer la figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Mots les plus fréquents dans les tweets négatifs', 
                fontsize=16, pad=20)
    
    return fig


def create_temporal_histogram(df: pd.DataFrame):
    """
    Crée un histogramme temporel du volume de tweets par heure/jour.
    
    Args:
        df: DataFrame avec les données analysées
        
    Returns:
        Figure Plotly
    """
    if 'date' not in df.columns:
        return None
    
    # Ajouter des colonnes pour le groupement temporel
    df_copy = df.copy()
    df_copy['date_only'] = df_copy['date'].dt.date
    df_copy['hour'] = df_copy['date'].dt.hour
    
    # Créer le graphique par date
    tweets_by_date = df_copy.groupby('date_only').size().reset_index(name='count')
    
    fig = px.bar(
        tweets_by_date,
        x='date_only',
        y='count',
        labels={'date_only': 'Date', 'count': 'Nombre de tweets'},
        color='count',
        color_continuous_scale='Reds',
        title='Volume de tweets par jour'
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Nombre de tweets",
        height=400,
        showlegend=False
    )
    
    return fig


def main():
    """
    Fonction principale du dashboard.
    """
    # En-tête
    st.markdown('<h1 class="main-header">Tesla Sentiment Analysis</h1>', 
                unsafe_allow_html=True)
    
    # Charger les données
    df = load_data()
    
    if df is None:
        return
    
    # Sidebar avec filtres
    st.sidebar.header("🔍 Filtres")
    
    # Filtre par sentiment
    sentiment_options = ['Tous'] + df['sentiment'].unique().tolist()
    selected_sentiment = st.sidebar.selectbox(
        "Sentiment",
        sentiment_options
    )
    
    # Filtre par date
    if 'date' in df.columns:
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        
        date_range = st.sidebar.date_input(
            "Période",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    # Appliquer les filtres
    df_filtered = df.copy()
    
    if selected_sentiment != 'Tous':
        df_filtered = df_filtered[df_filtered['sentiment'] == selected_sentiment]
    
    if 'date' in df.columns and len(date_range) == 2:
        df_filtered = df_filtered[
            (df_filtered['date'].dt.date >= date_range[0]) &
            (df_filtered['date'].dt.date <= date_range[1])
        ]
    
    # Métriques clés
    st.sidebar.markdown("---")
    st.sidebar.header("📊 Métriques")
    
    total_tweets = len(df_filtered)
    positive_pct = (df_filtered['sentiment'] == 'positive').sum() / total_tweets * 100 if total_tweets > 0 else 0
    negative_pct = (df_filtered['sentiment'] == 'negative').sum() / total_tweets * 100 if total_tweets > 0 else 0
    mean_polarity = df_filtered['polarity'].mean() if total_tweets > 0 else 0
    
    st.sidebar.metric("Total tweets", total_tweets)
    st.sidebar.metric("% Positifs", f"{positive_pct:.1f}%")
    st.sidebar.metric("% Négatifs", f"{negative_pct:.1f}%")
    st.sidebar.metric("Polarité moyenne", f"{mean_polarity:.3f}")
    
    # Corps principal du dashboard
    # Graphique camembert
    st.markdown("### 📊 Distribution des Sentiments")
    pie_fig = create_sentiment_pie_chart(df_filtered)
    st.plotly_chart(pie_fig, use_container_width=True)
    
    # Deux colonnes pour WordCloud et histogramme temporel
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ☁️ WordCloud des Tweets Négatifs")
        wordcloud_fig = create_wordcloud_negative(df_filtered)
        st.pyplot(wordcloud_fig)
    
    with col2:
        st.markdown("### 📅 Volume Temporel des Tweets")
        temporal_fig = create_temporal_histogram(df_filtered)
        if temporal_fig:
            st.plotly_chart(temporal_fig, use_container_width=True)
        else:
            st.info("Données temporelles non disponibles")
    
    # Section : Top 5 tweets les plus négatifs
    st.markdown("---")
    st.markdown("### 🔴 Top 5 Tweets les Plus Négatifs")
    
    # Obtenir les tweets négatifs et les trier par polarité
    negative_tweets = df_filtered[df_filtered['sentiment'] == 'negative'].copy()
    
    if len(negative_tweets) > 0:
        # Trier par polarité (les plus négatifs en premier)
        negative_tweets = negative_tweets.sort_values('polarity', ascending=True).head(5)
        
        for idx, (_, row) in enumerate(negative_tweets.iterrows(), 1):
            with st.expander(f"Tweet #{idx} - Polarité: {row['polarity']:.3f} | Likes: {row.get('likes', 0)} | RT: {row.get('retweets', 0)}"):
                st.write("**Texte original :**")
                st.write(row.get('text', 'N/A'))
                
                if 'text_cleaned' in row and pd.notna(row['text_cleaned']):
                    st.write("**Texte nettoyé :**")
                    st.write(row['text_cleaned'])
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Polarité", f"{row['polarity']:.3f}")
                with col_b:
                    vader_neg = row.get('vader_neg', row.get('vader_compound', 0))
                    st.metric("Score Négatif VADER", f"{vader_neg:.3f}")
                with col_c:
                    date_str = 'N/A'
                    if 'date' in row and pd.notna(row.get('date')):
                        try:
                            date_str = pd.to_datetime(row['date']).strftime('%Y-%m-%d')
                        except:
                            date_str = str(row['date'])
                    st.metric("Date", date_str)
                
                # Détecter le sarcasme si possible
                try:
                    analyzer = TeslaSentimentAnalyzer()
                    text_for_sarcasm = row.get('text', '')
                    if text_for_sarcasm:
                        sarcasm_indicators = analyzer.detect_sarcasm_indicators(text_for_sarcasm)
                        if sarcasm_indicators:
                            st.warning(f"⚠️ Indicateurs de sarcasme détectés: {', '.join(sarcasm_indicators)}")
                except:
                    pass
    else:
        st.info("Aucun tweet négatif trouvé avec les filtres sélectionnés.")
    
    # Informations supplémentaires
    st.markdown("---")
    with st.expander("ℹ️ Informations sur l'analyse"):
        st.markdown("""
        **Méthodes utilisées :**
        - **VADER** (Valence Aware Dictionary and sEntiment Reasoner) : Analyseur spécialisé pour les réseaux sociaux
        - **TextBlob** : Analyseur basé sur des règles avec scores de polarité et subjectivité
        
        **Classification :**
        - **Positif** : polarité > 0.1
        - **Négatif** : polarité < -0.1
        - **Neutre** : -0.1 ≤ polarité ≤ 0.1
        
        **Limites :**
        - La détection du sarcasme est basique et pourrait être améliorée
        - Les emojis sont partiellement pris en compte
        - Les contextes culturels ne sont pas toujours bien interprétés
        """)


if __name__ == "__main__":
    main()

