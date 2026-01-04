# 🚀 Guide de Démarrage Rapide - Dashboard Moderne

## Installation (1 minute)

```bash
pip install fastapi uvicorn[standard] python-multipart
```

Ou installez toutes les dépendances :

```bash
pip install -r requirements.txt
```

## Lancement (10 secondes)

```bash
./run_dashboard.sh
```

Ou directement :

```bash
python -m uvicorn src.dashboard_api:app --reload --host 0.0.0.0 --port 8000
```

## Accès

Ouvrez votre navigateur à : **http://localhost:8000**

C'est tout ! 🎉

---

## ✨ Ce que vous verrez

- 🎨 **Interface moderne** avec design épuré
- 📊 **4 métriques** en temps réel (Total, Positifs, Négatifs, Polarité)
- 📈 **2 graphiques interactifs** (Distribution, Volume temporel)
- ☁️ **WordCloud** des tweets négatifs
- 🔴 **Top 5 tweets** les plus négatifs
- 🔍 **Filtres** pour personnaliser l'analyse

---

## 🎯 Utilisation

1. **Utilisez les filtres** en haut de la page
2. **Cliquez sur "Appliquer les filtres"**
3. **Observez** la mise à jour en temps réel de tous les éléments

---

## ❓ Problème ?

**Le serveur ne démarre pas ?**

```bash
pip install fastapi uvicorn
```

**Erreur "Fichier introuvable" ?**

- Vérifiez que `data/tesla_sentiment_analysis.csv` existe
- Sinon, exécutez d'abord les phases 1-3 du projet

**Le dashboard est vide ?**

- Vérifiez la console du navigateur (F12)
- Vérifiez que le serveur tourne sur le port 8000

---

## 📚 Plus d'infos

Consultez [DASHBOARD_MODERNE.md](DASHBOARD_MODERNE.md) pour la documentation complète.
