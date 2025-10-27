# 📚 Documentation Architecture - Hello Pulse

## Structure de la Documentation

```
docs/
├── architecture/
│   ├── MCP/                            📡 Model Context Protocol
│   │   ├── MCP.md                      • Concepts MCP
│   │   └── MCP Server.md               • Configuration serveurs
│   │
│   ├── product/                        🎯 Définition Produit
│   │   ├── hello-pulse-product-definition.md
│   │   └── hello-pulse-architecture-dashboard-canvas.md
│   │
│   ├── agents/
│   │   └── ARCHITECTURE-FINALE.md          ⭐ Architecture agents validée
│   │
│   └── synthese-cocreation-opportunites-ia.md  📊 Méthodologies
│
└── README.md (ce fichier)
```

---

## 🎯 Documents par Thème

### Architecture des Agents ⭐ RÉFÉRENCE PRINCIPALE

**Fichier** : `docs/architecture/agents/ARCHITECTURE-FINALE.md`

**Contenu** :
- Architecture validée des 3 agents (Facilitateur, Assistant, Studio)
- Rôles et responsabilités détaillés
- Stack technique (Pydantic AI, Gemini, MCP)
- Configuration tools MCP par agent
- Coûts et performance
- Plan d'implémentation par phases

**Statut** : ✅ À jour et validé (Octobre 2025)

---

### Méthodologies de Co-création

**Fichier** : `docs/architecture/synthese-cocreation-opportunites-ia.md`

**Contenu** :
- Design Thinking (5 phases)
- Design Sprint (5 jours Google Ventures)
- Business Model Canvas
- Value Proposition Canvas
- Techniques de brainstorming (SCAMPER, Six Thinking Hats, etc.)
- Opportunités IA par phase/activité

**Utilité** : Guide pour implémenter les fonctionnalités IA dans Canvas

**Statut** : ✅ À conserver tel quel

---

### Définition Produit

**Fichier** : `docs/architecture/product/hello-pulse-product-definition.md`

**Contenu** :
- Vision globale Hello Pulse
- Problèmes identifiés
- Fonctionnalités core
- Positionnement marché
- Roadmap long terme

**Note** : Ce document présente la vision **produit** (features, UX, marché)
Notre architecture agents se concentre sur la partie **IA** uniquement.

**Statut** : ✅ À conserver (vision produit différente de tech)

---

### Model Context Protocol (MCP)

**Fichiers** :
- `docs/architecture/MCP/MCP.md` - Concepts
- `docs/architecture/MCP/MCP Server.md` - Configuration

**Contenu** :
- Explications protocole MCP
- Comment configurer serveurs MCP
- Intégration avec Pydantic AI

**Statut** : ✅ À conserver (documentation technique MCP)

---

## 🧭 Guide de Navigation

### Je veux comprendre...

**...l'architecture des agents IA** → `docs/agents/ARCHITECTURE-FINALE.md` ⭐

**...les méthodologies de co-création** → `docs/architecture/synthese-cocreation-opportunites-ia.md`

**...la vision produit globale** → `docs/architecture/product/hello-pulse-product-definition.md`

**...Quel sont les serveur mcp répérés** → `docs/architecture/MCP/`

---

### Je veux implémenter...

**...l'Agent Assistant** → Lire `docs/agents/ARCHITECTURE-FINALE.md` section "Agent 2"

**...l'Agent Facilitateur** → Lire `docs/agents/ARCHITECTURE-FINALE.md` section "Agent 1"

**...une fonctionnalité Canvas** → Lire `synthese-cocreation-opportunites-ia.md` pour les méthodologies

---

## 📋 Checklist Cohérence

Avant de coder, vérifier :

- ✅ L'architecture suit bien le document `ARCHITECTURE-FINALE.md`
- ✅ Les agents utilisent Pydantic AI (pas autre framework)
- ✅ Le Facilitateur n'a PAS de tools MCP (monitoring interne)
- ✅ L'Assistant a 3 tools : Tavily, RAG, Image Gen
- ✅ Le Studio a 10+ tools MCP (extensible)
- ✅ Pas de confusion entre vision produit et architecture technique

---

## 🔄 Mises à Jour

**Dernier update** : Octobre 2025

**Prochaines mises à jour** :
- Phase 1 : Canvas Assistant implémenté
- Phase 2 : Facilitateur Smart Monitoring
- Phase 3 : Studio AI complet

---

**Document maintenu par** : Équipe Hello Pulse AI