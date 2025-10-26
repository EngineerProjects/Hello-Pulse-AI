# Hello Pulse - Architecture MVP Finale

**Version 1.0** | Décembre 2025

---

## 🎯 Stack Technique

| Composant | Choix | Justification |
|-----------|-------|---------------|
| **Framework Agents** | Pydantic AI | MCP natif, Type-safe, Léger |
| **LLM Principal** | Gemini 2.0 Flash | 1M tokens, 25x moins cher GPT-4o |
| **Web Search** | Tavily AI | Optimisé LLM, 1000 req/mois gratuit |
| **Vector DB** | Qdrant | Open-source, Self-hosted |
| **Backend** | FastAPI | Async, Type-safe, WebSockets |
| **Frontend** | Next.js 14+ | React, SSR |
| **Database** | PostgreSQL | Relationnel, JSONB |
| **Cache** | Redis (Upstash) | Session state, Rate limiting |
| **Hosting** | Railway | Usage-based, Simple déploiement |

---

## 🏗️ Architecture Système

```
FRONTEND (Next.js/Vercel)
├─ Canvas Page (temps réel)
├─ Studio AI (chat longue-forme)
└─ Dashboard Projects
        │
        ▼
BACKEND API (FastAPI/Railway)
├─ Agent Facilitateur (Canvas)
├─ Agent Général (Q&A, recherche)
├─ Agent Studio (génération massive)
└─ Monitoring Proactif
        │
        ▼
SERVICES EXTERNES
├─ Gemini 2.0 Flash API (LLM)
├─ Tavily MCP (Web Search)
├─ Qdrant (Vector DB)
└─ PostgreSQL + Redis
```

---

## 🤖 Agents IA

### 1. Agent Facilitateur (Canvas Brainstorming)

**Rôle** : Facilitation sessions en temps réel

**Postures Dynamiques** :
- **Guide** : Encourage génération d'idées (divergence)
- **Provocateur** : Questions décalées si blocage
- **Médiateur** : Gestion conflits/tensions
- **Timekeeper** : Gestion transitions phases

**Configuration** :
- Model : Gemini 2.0 Flash
- Temperature : 0.7
- Context : 1M tokens (historique complet session)

---

### 2. Agent Général (Canvas & Studio)

**Rôle** : Assistant polyvalent Q&A, recherche

**Capacités** :
- Réponses questions méthodologiques
- Recherche web contextuelle (Tavily)
- Accès knowledge base (BMC, SCAMPER, etc.)

**Configuration** :
- Model : Gemini 2.0 Flash
- Temperature : 0.5
- Tools : Tavily MCP, Knowledge Base RAG

---

### 3. Agent Studio (Exploration Avancée)

**Rôle** : Génération massive, prototypage

**Capacités** :
- Génération 50+ variations SCAMPER
- Deep research multi-sources
- Mash-ups créatifs

**Configuration** :
- Model : Gemini 2.0 Flash
- Temperature : 0.8
- Max Tokens : 8192

---

## ⚡ Feature Phare : Monitoring Proactif

### Architecture Hybride (Coût Optimisé)

```
Background Job (30 secondes)
        │
        ▼
NIVEAU 1 : RÈGLES PYTHON ($0)
├─ Calcule métriques session
├─ Détecte situations problématiques
├─ Score d'alerte (0-100)
└─ Décision : Intervention ou non ?
        │
        ├─── Score < 30 → SILENT ($0)
        │
        └─── Score ≥ 30 → Triage
                │
                ├─── 70% → MESSAGE TEMPLATE ($0)
                │         (pause, timer, check-in)
                │
                └─── 30% → LLM PERSONNALISÉ ($0.0006)
                          (sollicitation, médiation)
```

### Détections Automatiques

**Participation** :
- Silencieux >15 min → Message privé (template)
- Silencieux >25 min → Sollicitation publique (LLM)
- Dominant >50% → Feedback privé (template)

**Énergie Groupe** :
- Baisse >30% → Observation
- Baisse >50% + 60 min → Suggestion pause (template)

**Timer** :
- <5 min phase → Alerte transition (template)

**Transitions** :
- Détection keywords convergence → Suggestion phase (LLM)

### Types d'Interventions

```
MESSAGES PRIVÉS (template) :
"👋 Hey [name], tout va bien ? N'hésite pas à partager tes idées !"

MESSAGES PUBLICS (LLM personnalisé) :
"[Name] a de l'expérience en [expertise]. J'aimerais connaître ton point de vue sur [sujet]."

SUGGESTIONS PAUSE (template) :
"⏸️ Vous travaillez depuis 90 minutes. Pause de 10 minutes ?"

TRANSITIONS PHASE (LLM) :
"🎯 32 idées générées ! Prêts à passer en phase Convergence ?"
```

---

## 💰 Estimation Coûts MVP (100 Users Actifs)

### APIs & Services

| Service | Usage Estimé | Coût/Mois |
|---------|--------------|-----------|
| **Gemini 2.0 Flash** | 500M input + 200M output tokens | $50 + $80 = **$130** |
| **Tavily API** | 1000 crédits/mois | **$0** (free tier) |
| **OpenAI Embeddings** | 50M tokens | **$1** |
| **Total APIs** | | **$131/mois** |

**Détail Gemini** :
- Input : $0.10 / 1M tokens
- Output : $0.40 / 1M tokens
- Agent proactif optimisé : ~70% templates ($0), 30% LLM

---

### Infrastructure

| Service | Plan | Coût/Mois |
|---------|------|-----------|
| **Railway Backend** | Hobby + usage | **$10-15** |
| **Railway PostgreSQL** | Hobby (inclus DB) | **$5** |
| **Upstash Redis** | Free tier (10K req/day) | **$0** |
| **Qdrant** | Self-hosted Docker (Railway) | **$5** |
| **Vercel Frontend** | Hobby | **$0** |
| **Total Infra** | | **$20-25/mois** |

**Note Railway** :
- Hobby : $5/mois + $5 crédit inclus
- Usage-based : ~$0.000463/GB-hour RAM, ~$0.000231/vCPU-hour
- Estimation : Backend (~$5-10) + PostgreSQL (~$5) + Qdrant (~$5)

---

### Monitoring & Tools

| Service | Plan | Coût/Mois |
|---------|------|-----------|
| **Sentry** | Developer (gratuit) | **$0** |
| **Pydantic Logfire** | Free tier | **$0** |
| **Better Uptime** | Free tier | **$0** |
| **Total Monitoring** | | **$0/mois** |

---

### 📊 Total Coûts MVP

```
APIs :            $131/mois
Infrastructure :   $25/mois
Monitoring :       $0/mois (free tiers)
─────────────────────────────
TOTAL :          $156/mois

Coût par user actif : $1.56/mois
```

### Projections Scaling

| Users | API | Infra | Total/Mois | Coût/User |
|-------|-----|-------|------------|-----------|
| **100** | $131 | $25 | **$156** | **$1.56** |
| **500** | $655 | $80 | **$735** | **$1.47** |
| **1000** | $1,310 | $150 | **$1,460** | **$1.46** |

**Observation** : Coût/user stable grâce à free tiers monitoring et infra usage-based

---

## 🚀 Fonctionnalités MVP

### Phase 1 : Core (Mois 1-3)

**Canvas Collaboratif** :
- ✅ Post-its temps réel (WebSocket <100ms)
- ✅ Clusters & connexions
- ✅ Timer & phases (Divergence/Convergence/Priorisation)
- ✅ Multi-users simultanés

**Agent Facilitateur** :
- ✅ Postures dynamiques (Guide/Provocateur/Médiateur)
- ✅ Monitoring proactif (30s)
- ✅ Messages privés/publics automatiques
- ✅ Détection participation/énergie

**Agent Général** :
- ✅ Q&A méthodologies
- ✅ Web search (Tavily)
- ✅ Knowledge base (BMC, VPC, SCAMPER)

**Templates** :
- ✅ Business Model Canvas
- ✅ Value Proposition Canvas
- ✅ Design Sprint

**Export** :
- ✅ PDF/PNG Canvas
- ✅ Synthèse automatique sessions

---

### Phase 2 : Intelligence (Mois 4-6)

**Studio AI** :
- Interface chat longue-forme
- Génération massive (50+ variations SCAMPER)
- Deep research multi-sources
- Mash-ups créatifs

**Clustering Automatique** :
- Regroupement idées similaires
- Labels automatiques (embeddings)
- Visualisation clusters

**Custom Agents** :
- Builder agents personnalisés
- Templates méthodologies custom

---

### Phase 3 : Avancé (Mois 7-10)

**Prototypage Visuel** :
- Wireframes automatiques (Dalle-3)
- Mockups interfaces

**Voice Mode** :
- Facilitation vocale temps réel
- STT/TTS intégré

**Intégrations** :
- Notion, Jira, Google Drive
- Export automatique

**Analytics** :
- Dashboard métriques avancées
- Patterns équipes

---

## 🎯 Avantages Compétitifs

### vs Miro/Mural/FigJam
❌ Canvas passif sans IA  
✅ **Hello Pulse** : Agent IA proactif + facilitation intelligente

### vs ChatGPT/Claude
❌ Réactif uniquement (attend requête)  
✅ **Hello Pulse** : Surveillance continue + interventions au bon moment

### Unique Value Proposition
🎯 **Seul outil avec agent facilitateur proactif**  
🎯 **Canvas + IA synchronisés en temps réel**  
🎯 **Monitoring intelligent participation/énergie**  
🎯 **Interventions personnalisées automatiques**

---

## 📅 Timeline MVP

| Sprint | Durée | Livrables |
|--------|-------|-----------|
| **1-2** | 4 sem | Infrastructure + Auth + DB |
| **3-4** | 4 sem | Agent Facilitateur basique |
| **5-6** | 4 sem | MCP + Tavily + Knowledge Base |
| **7-8** | 4 sem | Canvas Backend (WebSocket) |
| **9-11** | 6 sem | Canvas Frontend + UI |
| **12-13** | 4 sem | Templates + Export |
| **14** | 2 sem | Tests E2E + Launch Beta |

**Total : 14 sprints (28 semaines / ~7 mois)**

---

## 🔒 Sécurité & Compliance

**Authentification** :
- JWT tokens
- OAuth (Google, Microsoft)
- Row-level security PostgreSQL

**Data Privacy** :
- RGPD compliant
- Data retention configurable
- Export données utilisateur

**API Security** :
- Rate limiting (Redis)
- API keys rotation
- CORS configuré

---

## 📈 Métriques Succès MVP

### Techniques
- Latence agent : <2s (p95)
- Uptime : >99%
- Canvas sync : <100ms

### Business
- 50 beta users (3 mois)
- 200+ sessions créées
- 2000+ idées générées
- Retention 7J : >50%
- NPS : >40

### Coûts
- Coût/user/mois : <$2
- Budget API : <$200/mois
- Marge contribution : >70%

---

## 🛠️ Stack Détaillé

### Backend
```
FastAPI (Python 3.11+)
├─ Pydantic AI (agents)
├─ SQLAlchemy (ORM)
├─ Alembic (migrations)
├─ python-socketio (WebSocket)
└─ httpx (async HTTP)
```

### Frontend
```
Next.js 14+ (App Router)
├─ React 18+
├─ Tailwind CSS
├─ Zustand (state)
├─ React Query (server state)
├─ Socket.io client (real-time)
└─ Fabric.js (Canvas rendering)
```

### Infrastructure
```
Hosting :
├─ Backend : Railway (Docker)
├─ Frontend : Vercel (Edge)
└─ Static : Vercel CDN

Data :
├─ PostgreSQL : Railway managed
├─ Redis : Upstash serverless
└─ Qdrant : Self-hosted Docker

CI/CD :
├─ GitHub Actions
├─ Auto-deploy main branch
└─ Tests avant déploiement

Monitoring :
├─ Sentry (errors)
├─ Pydantic Logfire (LLM observability)
└─ Better Uptime (uptime)
```

---

## 🚦 Prochaines Étapes

### Semaine 1
1. Setup GitHub repo (monorepo)
2. Créer comptes APIs (Google AI Studio, Tavily)
3. Design schema DB détaillé
4. Setup Railway projet

### Semaine 2
1. FastAPI boilerplate
2. Premier agent Pydantic AI (test)
3. Appel Gemini API (Hello World)
4. Setup MCP Tavily

### Semaine 3-4
1. Agent Facilitateur MVP
2. Context management
3. WebSocket Canvas prototype
4. Déploiement staging

---

## 📚 Ressources

**Documentation** :
- Pydantic AI : https://ai.pydantic.dev
- Gemini API : https://ai.google.dev/docs
- Tavily : https://docs.tavily.com
- MCP Protocol : https://modelcontextprotocol.io

**Pricing** :
- Gemini : https://ai.google.dev/pricing
- Railway : https://railway.com/pricing
- Tavily : https://tavily.com/pricing

---

## ✅ Décisions Validées

✅ **Pydantic AI** (pas LangChain, pas CrewAI)  
✅ **Gemini 2.0 Flash** principal (pas GPT-4o systématique)  
✅ **MCP** pour tools (pas code custom)  
✅ **Agent unique multi-postures** (pas multi-agents)  
✅ **Monitoring proactif** avec règles + templates (pas SLM local)  
✅ **Railway** hosting (usage-based, simple)  
✅ **Free tiers maximum** pour monitoring (Sentry, Logfire, Uptime)

**Total coûts MVP : $156/mois pour 100 users** ✨

---

*Document technique validé - Prêt pour implémentation*
