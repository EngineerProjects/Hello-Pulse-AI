# 🎯 Hello Pulse AI

## Objectif
Agent IA général autonome capable de réaliser des tâches complexes grâce à l'intégration d'outils MCP (Model Context Protocol).

## Vision
- **Agent unique** : Focus sur l'agent General (recherche, analyse, génération)
- **MCP natif** : Utilisation optimale des serveurs MCP avec Pydantic AI
- **Simplicité** : Architecture minimaliste et extensible
- **Production ready** : Code propre, testé, documenté

## Architecture
```
Agent General ←→ MCP Manager ←→ [Tavily, Desktop Commander, Chrome, ...]
```

## Quick Start
```bash
# Installation
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Éditer .env avec vos clés API

# Test
python main.py
```

## MCP Tools Intégrés
- **🔍 Tavily** : Recherche web intelligente  
- **💻 Desktop Commander** : Automatisation système
- **🌐 Chrome** : Automatisation navigateur

---
*Build with ❤️ using Pydantic AI + MCP*
