# 🏗️ Architecture des Agents IA - Hello Pulse
## Architecture Finale Validée

**Version 3.0** | Octobre 2025  
**Statut** : ✅ Architecture validée et prête à implémenter

---

## 📋 Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Architecture par Page](#architecture-par-page)
3. [Agents Détaillés](#agents-détaillés)
4. [Stack Technique](#stack-technique)
5. [Coûts et Performance](#coûts-et-performance)
6. [Plan d'Implémentation](#plan-dimplémentation)

---

## 🎯 Vue d'Ensemble

Hello Pulse dispose de **3 agents IA distincts** répartis sur **2 pages** :

```
PAGE CANVAS (Collaboration Temps Réel)
├─ 🎭 Agent Facilitateur (Proactif)
│  • Monitoring & Interventions
│  • ReAct: ❌ NON
│  • Tools: Aucun
│  • Coût: ~$0.0005/session
│
└─ 💬 Agent Assistant (Réactif)
   • Q&A rapide avec recherche
   • ReAct: ✅ Léger
   • Tools: Tavily, RAG, Image Gen
   • Coût: ~$0.005/réponse

              ↓ Transition ↓
      [Bouton "Approfondir dans Studio AI"]
              ↓

PAGE STUDIO AI (Recherche Approfondie)
└─ 🤖 Agent Studio (Avancé)
   • Deep Research & Prototypage
   • ReAct: ✅ Complet
   • Tools: 10+ MCP servers
   • Coût: ~$0.01-0.05/session
```

---

## 🎨 Architecture par Page

### PAGE CANVAS - Espace de Co-création

**Interface** : Whiteboard collaboratif style Miro avec sticky notes, dessins, templates

**Objectif** : Faciliter les sessions de brainstorming et exercices de co-création en temps réel

**Agents présents** :
- 🎭 Facilitateur (proactif, monitoring)
- 💬 Assistant (réactif, Q&A)

**Fonctionnalités** :
- Templates méthodologiques (Design Thinking, BMC, SCAMPER, etc.)
- Collaboration temps réel multi-utilisateurs
- Sticky notes, dessins, votes
- Capture audio/vidéo des sessions
- Génération d'idées assistée par IA
- Clustering automatique

---

### PAGE STUDIO AI - Espace de Recherche Avancée

**Interface** : Dashboard avec interface conversationnelle et outils avancés

**Objectif** : Recherche approfondie, prototypage, et création complexe

**Agent présent** :
- 🤖 Studio (ReAct complet, tous les tools)

**Fonctionnalités** :
- Deep research multi-sources (10-20 sources)
- Prototypage web (HTML/CSS/JS temporaire)
- Modélisation 3D (Blender)
- Navigation web automatisée (style Manus AI)
- Génération de documents (Desktop Commander)
- Création d'agents custom
- Génération d'images avancées

**Connexion avec Canvas** :
- Accessible via bouton dans Canvas
- Context de session transféré automatiquement
- Travail en équipe ou individuel

---

## 🎭 Agents Détaillés

### AGENT 1 : FACILITATEUR (Canvas - Proactif)

#### Rôle
Accompagnateur humain proactif qui guide les sessions sans interventions coûteuses.

#### Caractéristiques
```yaml
Mode: Proactif (intervient automatiquement)
ReAct: ❌ NON (pas besoin)
Tools_MCP: [] (aucun - monitoring interne)
Coût: ~$0.0005 par session de 2h
Temperature: 0.7
Max_tokens: 2048
```

#### Monitoring "Smart Rules"

**Principe** : Règles backend sans coût + LLM seulement pour générer messages

```yaml
Métriques calculées (côté backend, coût $0):
  - silence_duration: Par utilisateur
  - post_it_count: Contributions par user
  - phase_duration: Timer de session
  - energy_score: Basé sur activité

Règles de détection (sans LLM):
  - Silence > 15 min → Alert "silence_warning"
  - Phase > 60 min → Alert "break_suggestion"
  - User > 50% contributions → Alert "dominant_user"
  - Energy < 30% → Alert "energy_low"

Intervention (SEULEMENT quand alerte):
  - LLM appelé UNIQUEMENT pour générer le message
  - Context: Alert + session state + recent post-its
  - Coût: ~$0.0001 par intervention
```

#### Postures Dynamiques

```yaml
guide:
  description: "Encourage créativité et divergence"
  usage: "Phase d'idéation, brainstorming"
  
provocateur:
  description: "Challenge avec questions dérangeantes"
  usage: "Déblocage créatif, sortir du cadre"
  
timekeeper:
  description: "Surveille le temps et transitions"
  usage: "Gestion des phases de session"
  
# FUTUR (Phase 2)
mediateur:
  description: "Gère tensions et conflits"
  usage: "Détection de désaccords"
  implementation: "Nécessite analyse sentiment audio/texte"
```

#### Interventions Types

```
Exemples de messages générés:
- "Alice, on n'a pas encore entendu ton avis. Qu'en penses-tu ?"
- "Vous travaillez depuis 60 minutes. Une pause de 10 min ?"
- "25 idées générées ! Prêts pour la phase de Convergence ?"
- "Et si on faisait exactement l'inverse ?" (Provocateur)
```

---

### AGENT 2 : ASSISTANT (Canvas - Réactif)

#### Rôle
Répondeur intelligent avec recherche pour questions rapides et visualisations simples.

#### Caractéristiques
```yaml
Mode: Réactif (répond quand sollicité via @Assistant)
ReAct: ✅ Léger (Pydantic AI natif avec tools)
Tools_MCP: [tavily, knowledge_base, dalle3]
Coût: ~$0.005 par réponse complexe
Temperature: 0.6 (plus factuel)
Max_tokens: 2048
```

#### Capacités

```yaml
Q&A Conversationnel:
  - Réponses sur méthodologies (Design Thinking, SCAMPER)
  - Informations entreprise (données internes)
  - Clarifications de concepts
  - Exemples pratiques

Recherche d'Information:
  - Web search (Tavily) pour infos récentes
  - RAG knowledge base (méthodologies)
  - RAG entreprise (documents internes)

Génération Visuelle Simple:
  - Storyboards (2-4 frames)
  - Wireframes basiques
  - Icônes et illustrations
  - Visualisations de concepts
```

#### Tools MCP

**Tool 1: Tavily (Web Search)**
- Usage: Informations récentes, tendances, actualités
- Exemple: "Quelles sont les tendances IA en 2025 ?"

**Tool 2: Knowledge Base (RAG)**
- Sources:
  - Méthodologies co-création
  - Documents entreprise
- Exemple: "Comment appliquer SCAMPER dans notre contexte ?"

**Tool 3: Image Generation (DALL-E 3)**
- Usage: Visualisations rapides, storyboards
- Exemple: "Génère un storyboard pour cette idée d'app"

#### Workflow ReAct

```
User: "Montre-moi les tendances IA 2025 en image"

Pydantic AI gère automatiquement:
  [Reasoning] User veut infos récentes + visualisation
  [Action 1] Tool "web_search" → "AI trends 2025"
  [Observation] Agents autonomes, multimodal, edge AI
  [Action 2] Tool "generate_simple_image" → Description
  [Observation] Image créée
  [Final] Synthèse avec tendances + image
```

---

### AGENT 3 : STUDIO (Studio AI - Avancé)

#### Rôle
Agent de recherche approfondie et prototypage complexe.

#### Caractéristiques
```yaml
Mode: Réactif (accessible depuis Canvas ou directement)
ReAct: ✅ Complet avec reasoning explicite
Tools_MCP: 10+ servers (extensible)
Coût: ~$0.01-0.05 par session approfondie
Temperature: 0.8 (plus créatif)
Max_tokens: 8192 (contenu long)
```

#### Capacités Avancées

```yaml
Deep Research:
  - Recherche multi-sources (10-20 sources)
  - Navigation web automatisée
  - Synthèse approfondie
  - Analyse comparative

Prototypage:
  - Web apps temporaires (HTML/CSS/JS)
  - Modèles 3D (Blender)
  - Wireframes interactifs
  - Animations

Gestion Documents:
  - Lecture/écriture fichiers
  - Rapports, business plans
  - Export multi-formats

Génération Créative:
  - Images avancées
  - 50+ variations SCAMPER
  - Storyboards animés

Création Agents:
  - Builder agents custom
  - Configuration prompts/tools
  - Templates sectoriels
```

#### Tools MCP par Phase

**Phase 1 (MVP):**
- tavily: Web search avancée
- filesystem: Desktop Commander (read/write docs)
- puppeteer: Web browser automation

**Phase 2 (Post-MVP):**
- e2b: Code interpreter sécurisé
- dalle3: Image generation avancée
- knowledge_base: RAG complet

**Phase 3 (Innovation):**
- blender: Modélisation 3D
- github: Version control
- notion/linear: Intégrations
- figma: Import designs

---

## 🛠️ Stack Technique

### Framework IA

```yaml
Framework: Pydantic AI (v1.4.0+)

Justification:
  - Built by Pydantic Team
  - Type-safe avec validation
  - MCP integration native
  - Dependency injection propre
  - Léger (pas de couches inutiles)
  - ReAct implicite via tools
```

### LLM Principal

```yaml
Modèle: Gemini 2.0 Flash
Provider: Google AI

Justification:
  - Performance/coût optimal
  - Multimodal (texte + images)
  - Context window large (1M tokens)
  - Latence faible
  - Pricing compétitif
```

### Configuration par Agent

```yaml
Facilitateur:
  model: gemini-2.0-flash
  temperature: 0.7
  max_tokens: 2048
  tools_mcp: []
  
Assistant:
  model: gemini-2.0-flash
  temperature: 0.6
  max_tokens: 2048
  tools_mcp: [tavily, knowledge_base, dalle3]
  
Studio:
  model: gemini-2.0-flash
  temperature: 0.8
  max_tokens: 8192
  tools_mcp: [tavily, filesystem, puppeteer, ...]
```

### MCP (Model Context Protocol)

```yaml
Enabled: true
Config_file: mcp_config.json

Servers configurés:
  - Tavily: Web search (déjà actif)
  - Filesystem: À ajouter (Desktop Commander)
  - Puppeteer: À ajouter (Web browser)
  - Autres: Phase 2+
```

---

## 💰 Coûts et Performance

### Coûts par Agent

| Agent | Coût par Utilisation | Fréquence | Coût Session 2h |
|-------|---------------------|-----------|-----------------|
| **Facilitateur** | $0.0001/intervention | 5 interventions | $0.0005 |
| **Assistant** | $0.005/réponse | 10 questions | $0.05 |
| **Studio** | $0.02/recherche | 2 recherches | $0.04 |
| **TOTAL** | - | - | **~$0.09** |

### Justification Coûts Facilitateur

**Pourquoi si bas ?**
- Monitoring = règles backend ($0)
- LLM appelé SEULEMENT pour générer messages
- 5 interventions typiques par session
- Pas d'analyse audio continue (trop cher)
- Pas de monitoring vidéo (trop cher)

**Médiateur reporté en Phase 2** :
- Nécessite analyse sentiment (audio/texte)
- Coûts élevés pour peu de valeur immédiate
- Attendre meilleure solution technique

---

## 📅 Plan d'Implémentation

### Phase 1 : Canvas Assistant (PRIORITÉ IMMÉDIATE)

**Objectif** : Agent Assistant fonctionnel avec ReAct

**Tâches** :
1. Créer structure `hello_pulse/agents/assistant/`
2. Implémenter agent avec Pydantic AI + 3 tools
3. Créer prompts système
4. Intégrer Tavily (déjà configuré)
5. Créer RAG tool (méthodologies + entreprise)
6. Créer Image Gen tool (DALL-E 3)
7. Tester dans Canvas CLI

**Durée estimée** : 1-2 semaines

---

### Phase 2 : Amélioration Facilitateur

**Objectif** : Système de monitoring proactif intelligent

**Tâches** :
1. Implémenter boucle monitoring backend
2. Créer règles de détection (FacilitatorRules)
3. Système d'interventions contextuelles
4. Changement posture automatique
5. Dashboard métriques temps réel
6. Tests avec sessions réelles

**Durée estimée** : 2-3 semaines

---

### Phase 3 : Studio AI (Long terme)

**Objectif** : Agent Studio avec tools avancés

**Tâches** :
1. Créer page Studio dans dashboard
2. Agent Studio avec ReAct complet
3. Intégrer tools MCP prioritaires
4. Connexion Canvas → Studio (context transfer)
5. Système de prototypage web
6. Agent Builder (création agents custom)

**Durée estimée** : 4-6 semaines

---

## 🔑 Points Clés à Retenir

### Architecture Validée

✅ **3 agents distincts** avec rôles clairs et complémentaires  
✅ **Pydantic AI** pour tous (type-safe, MCP natif)  
✅ **ReAct** où nécessaire (Assistant, Studio) pas où inutile (Facilitateur)  
✅ **Coûts maîtrisés** via smart monitoring  
✅ **Scalable** et extensible (MCP tools modulaires)

### Pas de Confusion

❌ **PAS de 4 agents métier** (c'était une erreur de compréhension)  
❌ **PAS de ReAct partout** (seulement où il apporte valeur)  
❌ **PAS de monitoring audio continu** (trop cher, peu de valeur)  
❌ **PAS d'architecture ReAct complexe** (Pydantic AI gère nativement)

### Priorités Claires

🔥 **Phase 1** : Canvas Assistant (immédiat)  
⏭️ **Phase 2** : Facilitateur Smart Monitoring  
🔮 **Phase 3** : Studio AI complet

---

**Document vivant** - Mis à jour selon implémentation  
**Contact** : Équipe Hello Pulse AI