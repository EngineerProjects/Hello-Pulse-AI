# 💬 Hello Pulse - Système de Chat

Interface de chat pour tester et interagir avec l'agent facilitateur IA.

## 🚀 Démarrage Rapide

### Lancer le chat interactif

```bash
python chat.py
```

### Lancer les tests

```bash
python tests/test_chat_session.py
```

## 📖 Commandes Disponibles

| Commande | Description |
|----------|-------------|
| `/help` | Afficher l'aide |
| `/posture` | Changer la posture de l'agent (Guide, Provocateur, Médiateur, Timekeeper) |
| `/history` | Afficher l'historique de conversation |
| `/stats` | Afficher les statistiques de la session |
| `/context` | Afficher le contexte de session actuel |
| `/clear` | Effacer l'historique |
| `/debug` | Activer/désactiver le mode debug |
| `/quit` | Quitter le chat |

## 🎭 Postures de l'Agent

### 1. Guide (par défaut)
**Rôle** : Encourager la génération d'idées et la divergence créative

**Comportement** :
- Pose des questions ouvertes stimulantes
- Célèbre les idées originales
- Encourage l'exploration de différentes directions
- Crée un espace sûr pour partager des idées "folles"

**Exemples** :
- "Excellente idée ! Que se passerait-il si on allait encore plus loin ?"
- "J'aime cette direction. Quelqu'un a une variation ou une idée complémentaire ?"

### 2. Provocateur
**Rôle** : Challenger les idées pour stimuler la créativité

**Comportement** :
- Pose des questions dérangeantes
- Encourage à voir les choses différemment
- Propose des scénarios extrêmes
- Challenge les idées conventionnelles

**Exemples** :
- "Et si on faisait exactement l'inverse ?"
- "Cette idée est intéressante, mais qu'est-ce qui pourrait la rendre complètement folle ?"

### 3. Médiateur
**Rôle** : Gérer les tensions et maintenir une atmosphère collaborative

**Comportement** :
- Détecte et apaise les tensions
- Rappelle les objectifs communs
- Valorise les différents points de vue
- Encourage l'écoute mutuelle

**Exemples** :
- "Je vois que vous avez des perspectives différentes, et c'est une richesse."
- "Prenons un moment pour écouter ce que [nom] essaie d'exprimer."

### 4. Timekeeper
**Rôle** : Gérer le temps et les transitions entre phases

**Comportement** :
- Surveille le temps et la progression
- Alerte sur les fins de phase
- Suggère des transitions opportunes
- Maintient le rythme et l'énergie

**Exemples** :
- "⏰ Il reste 5 minutes pour cette phase. Dernières idées ?"
- "Vous avez généré 25 idées en 30 minutes ! Prêts à passer en convergence ?"


## 📊 Mode Debug

Activer le mode debug avec `/debug` pour voir les informations détaillées :
- Type de message (public/private/system)
- Posture actuelle
- Type d'intervention
- Utilisateur cible

## 💾 Historique des Sessions

Les historiques sont automatiquement sauvegardés dans :
```
chat_histories/session-{timestamp}.json
```

Format :
```json
{
  "session_id": "session-20250101-120000",
  "current_posture": "guide",
  "messages": [
    {
      "role": "user",
      "content": "Message utilisateur",
      "timestamp": "2025-01-01T12:00:00"
    },
    {
      "role": "agent",
      "content": "Réponse de l'agent",
      "timestamp": "2025-01-01T12:00:05",
      "response": {
        "message_type": "public",
        "current_posture": "guide",
        "intervention_type": null
      }
    }
  ],
  "last_updated": "2025-01-01T12:00:05"
}
```

## 🔧 Architecture Technique

### ChatSession
Classe principale pour gérer une session de chat :
- Gestion de l'historique
- Changement de posture dynamique
- Sauvegarde/chargement automatique
- Statistiques et métriques

### CLI Interface
Interface en ligne de commande avec :
- Couleurs ANSI pour meilleure lisibilité
- Gestion des commandes interactives
- Mode debug
- Gestion propre des interruptions

## 🎯 Cas d'Usage

### Test de Prompts
Utilise le chat pour tester et affiner les prompts de chaque posture :

```bash
python chat.py
> /posture
Choisir (1-4): 1
> Comment générer plus d'idées créatives ?
```

### Simulation de Session
Simule différents scénarios de brainstorming :

```bash
> Un participant est silencieux depuis 15 minutes
> L'énergie du groupe semble baisser
> Nous avons 30 idées, devons-nous passer à la convergence ?
```

### Développement de Features
Base pour futures fonctionnalités :
- Studio AI (génération massive)
- Agent Général (Q&A + recherche)
- Monitoring proactif

## 📝 Notes de Développement

### État Actuel
✅ Chat interactif fonctionnel
✅ Changement de posture dynamique
✅ Sauvegarde historique
✅ Contexte de session mock
⏳ Monitoring proactif (à venir)
⏳ WebSocket temps réel (à venir)

### Prochaines Étapes
1. **Monitoring Proactif** : Background job + détection automatique
2. **Canvas Backend** : WebSocket + synchronisation temps réel
3. **Agent Général** : Q&A + recherche web (Tavily)
4. **Studio AI** : Génération massive + deep research

## 🐛 Debug et Troubleshooting

### Problème : Clé API non trouvée
```bash
ValueError: GOOGLE_API_KEY not found in environment
```
**Solution** : Vérifier que `.env` contient `GOOGLE_API_KEY=...`

### Problème : Warning additionalProperties
**Solution** : Déjà corrigé - pas de champs `dict` dans les output types

### Problème : Import errors
**Solution** : Vérifier que toutes les dépendances sont installées
```bash
pip install -r requirements.txt
```

## 📚 Ressources

- [Documentation Pydantic AI](https://ai.pydantic.dev)
- [Architecture MVP](../docs/hello-pulse-mvp-architecture-finale.md)
- [Prompts Facilitateur](../prompts/facilitator/)
