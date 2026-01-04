# 🎨 Dashboard Moderne - FastAPI + Tailwind CSS

## Vue d'ensemble

Le nouveau dashboard moderne offre une expérience utilisateur épurée et interactive avec :

- **Design moderne** : Interface épurée avec Tailwind CSS
- **Graphiques interactifs** : Chart.js pour des visualisations fluides
- **API RESTful** : Backend FastAPI performant
- **Responsive** : Adapté à tous les écrans (desktop, tablette, mobile)
- **Temps réel** : Mise à jour dynamique des données

## 🚀 Lancement Rapide

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Lancer le dashboard

**Option 1 : Script de lancement (Recommandé)**

```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

**Option 2 : Commande directe**

```bash
python -m uvicorn src.dashboard_api:app --reload --host 0.0.0.0 --port 8000
```

### Accès au dashboard

Une fois lancé, ouvrez votre navigateur à :

**http://localhost:8000**

## ✨ Fonctionnalités

### 1. Interface Moderne

- Design épuré avec Tailwind CSS
- Animations et transitions fluides
- Cards avec effet hover
- Gradient moderne pour le header

### 2. Métriques en Temps Réel

- **Total Tweets** : Nombre total de tweets analysés
- **Positifs** : Pourcentage de tweets positifs
- **Négatifs** : Pourcentage de tweets négatifs
- **Polarité Moyenne** : Score de polarité moyen

### 3. Graphiques Interactifs

#### Distribution des Sentiments (Donut Chart)

- Graphique en donut avec Chart.js
- Couleurs personnalisées (vert/rouge/gris)
- Affichage des pourcentages
- Légende interactive

#### Volume Temporel

- Histogramme des tweets par jour
- Visualisation de l'évolution dans le temps
- Zoom et interaction possibles

### 4. WordCloud

- Nuage de mots généré depuis les tweets négatifs
- Mise à jour automatique selon les filtres
- Image haute qualité

### 5. Top 5 Tweets Négatifs

- Liste des tweets les plus négatifs
- Affichage des métriques (likes, retweets, polarité)
- Design en cards avec bordures colorées

### 6. Filtres Interactifs

- **Filtre par sentiment** : Tous, Positif, Négatif, Neutre
- **Filtre par date** : Date de début et de fin
- Mise à jour automatique de tous les graphiques

## 🏗️ Architecture

### Backend (FastAPI)

**Fichier** : `src/dashboard_api.py`

**Endpoints API** :

- `GET /` : Page HTML du dashboard
- `GET /api/data` : Données brutes (avec filtres)
- `GET /api/stats` : Statistiques agrégées
- `GET /api/sentiment-distribution` : Distribution pour le graphique
- `GET /api/temporal-data` : Données temporelles
- `GET /api/top-negative` : Top N tweets négatifs
- `GET /api/wordcloud` : Image WordCloud en base64

### Frontend (HTML + Tailwind CSS)

**Fichier** : `dashboard_static/index.html`

**Technologies** :

- **Tailwind CSS** : Framework CSS utilitaire (via CDN)
- **Chart.js** : Bibliothèque de graphiques
- **Font Awesome** : Icônes
- **Vanilla JavaScript** : Pas de framework JS lourd

## 📁 Structure des Fichiers

```
tesla_sentiment_analysis/
├── src/
│   └── dashboard_api.py          # Serveur FastAPI
├── dashboard_static/
│   └── index.html                # Frontend HTML
├── run_dashboard_modern.sh       # Script de lancement
└── requirements.txt              # Dépendances (FastAPI, uvicorn)
```

## 🎨 Personnalisation

### Modifier les Couleurs

Les couleurs sont définies dans `dashboard_static/index.html` :

**Couleurs des sentiments** :

- Positif : `#10b981` (vert)
- Négatif : `#ef4444` (rouge)
- Neutre : `#6b7280` (gris)

**Gradient du header** :

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Modifier les Graphiques

Les graphiques utilisent Chart.js. Vous pouvez personnaliser les options dans les fonctions JavaScript :

- `loadSentimentDistribution()` : Graphique donut
- `loadTemporalData()` : Histogramme temporel

### Ajouter de Nouvelles Fonctionnalités

1. **Ajouter un endpoint API** dans `src/dashboard_api.py`
2. **Créer la fonction JavaScript** pour appeler l'endpoint
3. **Ajouter l'élément HTML** dans `dashboard_static/index.html`

## 🔧 Configuration

### Changer le Port

Modifiez le script de lancement ou utilisez :

```bash
uvicorn src.dashboard_api:app --reload --port 8080
```

### Mode Production

Pour un déploiement en production :

```bash
uvicorn src.dashboard_api:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🐛 Dépannage

### Le dashboard ne se charge pas

1. Vérifiez que le serveur est lancé : `http://localhost:8000`
2. Vérifiez la console du navigateur (F12) pour les erreurs
3. Vérifiez que les fichiers CSV existent dans `data/`

### Les graphiques ne s'affichent pas

1. Vérifiez que Chart.js est chargé (console navigateur)
2. Vérifiez que les données sont retournées par l'API
3. Testez les endpoints API directement : `http://localhost:8000/api/stats`

### Erreur CORS

Le middleware CORS est configuré pour autoriser toutes les origines. Si vous avez des problèmes, vérifiez la configuration dans `dashboard_api.py`.

### Le WordCloud ne s'affiche pas

1. Vérifiez qu'il y a des tweets négatifs dans les données
2. Vérifiez que `wordcloud` est installé : `pip install wordcloud`
3. Vérifiez les logs du serveur pour les erreurs

## 📊 Comparaison avec Streamlit

| Fonctionnalité       | Streamlit | Dashboard Moderne   |
| -------------------- | --------- | ------------------- |
| Design               | Basique   | Moderne et épuré    |
| Personnalisation CSS | Limitée   | Complète (Tailwind) |
| Performance          | Moyenne   | Excellente          |
| Interactivité        | Bonne     | Excellente          |
| Responsive           | Moyen     | Excellent           |
| API REST             | Non       | Oui                 |
| Déploiement          | Facile    | Facile              |

## 🚀 Déploiement

### Sur un serveur local

```bash
./run_dashboard_modern.sh
```

### Sur un serveur distant

1. Transférez les fichiers sur le serveur
2. Installez les dépendances
3. Lancez avec uvicorn
4. Configurez un reverse proxy (nginx) si nécessaire

### Avec Docker (optionnel)

Créez un `Dockerfile` :

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src.dashboard_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 Notes

- Le dashboard moderne utilise des CDN pour Tailwind CSS, Chart.js et Font Awesome
- Pour un usage hors ligne, téléchargez ces bibliothèques localement
- Les données sont chargées depuis les fichiers CSV dans `data/`
- Le serveur supporte le hot-reload en mode développement

## ✅ Avantages du Dashboard Moderne

✅ **Design épuré et professionnel**
✅ **Performance optimale**
✅ **API RESTful réutilisable**
✅ **Facilement extensible**
✅ **Responsive et moderne**
✅ **Graphiques interactifs**
✅ **Code maintenable**
