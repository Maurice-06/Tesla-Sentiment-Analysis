#!/bin/bash

# Script pour lancer le dashboard moderne FastAPI + Tailwind CSS
# Usage: ./run_dashboard_modern.sh

echo "🚗 Lancement du Dashboard Moderne Tesla Sentiment Analysis..."
echo ""

# Vérifier que FastAPI est installé
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ FastAPI n'est pas installé."
    echo "💡 Installation des dépendances..."
    pip install fastapi uvicorn[standard] python-multipart
fi

# Vérifier que uvicorn est installé
if ! python -c "import uvicorn" 2>/dev/null; then
    echo "💡 Installation de uvicorn..."
    pip install uvicorn[standard]
fi

echo "📊 Démarrage du serveur FastAPI..."
echo "🌐 Le dashboard sera accessible sur: http://localhost:8000"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur."
echo ""

# Lancer le serveur
python -m uvicorn src.dashboard_api:app --reload --host 0.0.0.0 --port 8000

