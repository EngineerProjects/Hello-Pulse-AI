# 🎯 Hello Pulse AI

**Agent facilitateur intelligent pour sessions de brainstorming collaboratif**

Partie IA du projet Hello Pulse - Facilitation de sessions créatives en temps réel avec monitoring proactif.

---

## 🚀 Installation Rapide

### Prérequis
- Python 3.11+
- Conda (recommandé) ou venv
- Clés API : Google Gemini, Tavily

### Configuration

1. **Cloner et installer les dépendances**
```bash
git clone [votre-repo]
cd Hello_pulse_ai
pip install -r requirements.txt
```

2. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env et ajouter vos clés API :
# - GOOGLE_API_KEY (Gemini)
# - TAVILY_API_KEY (Web search)
```

3. **Vérifier l'installation**
```bash
python verify_setup.py
```

4. **Lancer le chat de test**
```bash
python chat.py
```

---

## 📁 Structure du Projet

```
hello_pulse/
├── agents/                 # Agents IA
│   └── facilitator/       # Agent facilitateur (Canvas)
├── chat/                  # Système de chat
├── data_providers/        # Fournisseurs de données
├── mcp/                   # Model Context Protocol
├── models/                # Schémas Pydantic
├── prompts/               # Prompts des agents
└── config.py              # Configuration centralisée
```

---

## 🎭 Agent Facilitateur

### Postures Dynamiques
- **Guide** : Encourage la créativité et la divergence
- **Provocateur** : Challenge les idées avec questions dérangeantes
- **Médiateur** : Gère les tensions et maintient l'harmonie
- **Timekeeper** : Surveille le temps et les transitions

### Capacités
- Monitoring participation des membres
- Détection des silences prolongés
- Suivi de l'énergie du groupe
- Suggestions de transitions de phase

---

## 🛠️ Technologies

| Composant | Choix | Version |
|-----------|-------|---------|
| Framework Agents | Pydantic AI | 1.4.0 |
| LLM Principal | Gemini 2.0 Flash | - |
| Web Search | Tavily MCP | - |
| Config | YAML | 6.0+ |

---

## 💬 Utilisation du Chat CLI

```bash
python chat.py
```

### Commandes disponibles
- `/help` - Afficher l'aide
- `/posture` - Changer la posture de l'agent
- `/context` - Voir le contexte de session actuel
- `/history` - Afficher l'historique
- `/debug` - Activer le mode debug
- `/quit` - Quitter

---

## 📊 MockDataProvider

Pendant le développement, le système utilise des données simulées :
- Équipe aléatoire de 3-10 membres générée au démarrage
- Métriques qui évoluent dans le temps
- Simulation réaliste de participation, silences, énergie

Configuration dans `config.yml` :
```yaml
data_providers:
  mock:
    random_mode: true
    team_size:
      min: 3
      max: 10
```

---

## 🔧 Configuration

Le fichier `config.yml` centralise toute la configuration :
- Paramètres des agents (model, temperature, tokens)
- Postures disponibles
- Seuils de monitoring
- Configuration MCP
- Data providers

---

## 🧪 Vérification du Setup

Le script `verify_setup.py` vérifie automatiquement :
- ✅ Imports de tous les modules
- ✅ Configuration valide
- ✅ Fichiers prompts présents
- ✅ MockDataProvider fonctionnel

---

## 📝 État du Projet

### ✅ Implémenté
- Agent Facilitateur avec 4 postures
- Système de chat avec historique
- MockDataProvider pour développement
- Configuration MCP (Tavily)
- CLI de test interactif

### ⏳ En Développement
- Monitoring proactif automatique
- Agent Studio (recherche approfondie)
- API backend
- Canvas WebSocket temps réel

---

## 🔑 Variables d'Environnement

Voir `.env.example` pour la liste complète.

**Obligatoires :**
- `GOOGLE_API_KEY` - API Google Gemini
- `TAVILY_API_KEY` - API Tavily pour recherche web

---

## 📚 Documentation Complète

Pour plus de détails sur l'architecture et les décisions techniques, voir :
- `docs/hello-pulse-mvp-architecture-finale.md` - Architecture complète
- `hello_pulse/chat/README.md` - Documentation du système de chat
- `hello_pulse/prompts/facilitator/` - Prompts des postures

---

## 🤝 Contribution

Projet en cours de développement initial.

---

## 📄 Licence

[À définir]
