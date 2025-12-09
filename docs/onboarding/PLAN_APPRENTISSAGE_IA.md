# Plan d'Apprentissage : De Zéro à Transformer

Ce document présente un plan d'apprentissage structuré pour maîtriser le Deep Learning, en partant des bases mathématiques jusqu'à l'implémentation de modèles avancés comme les Transformers. Chaque étape est conçue pour lier la théorie à la pratique en Python, sans utiliser de librairies de haut niveau dans un premier temps.

---

### **Phase 1 : Les Fondations (Essentiel)**

1.  **Mathématiques pour le Machine Learning :**
    *   **Algèbre Linéaire :**
        *   *Concepts :* Scalaires, vecteurs, matrices, tenseurs. Opérations (addition, multiplication). Transposée, inverse, déterminant. Décomposition en valeurs propres (eigen-decomposition), SVD.
        *   *Projet Pratique :* Créer une petite librairie Python pour manipuler des vecteurs et des matrices (opérations de base) sans utiliser NumPy/PyTorch.
    *   **Calcul Différentiel :**
        *   *Concepts :* Dérivées, dérivées partielles, règle de la chaîne (chain rule), gradients.
        *   *Projet Pratique :* Implémenter le calcul de gradients pour des fonctions simples en Python.
    *   **Probabilités et Statistiques :**
        *   *Concepts :* Probabilité conditionnelle, théorème de Bayes, distributions (Gaussienne, Bernoulli), moyenne, variance, corrélation.
        *   *Projet Pratique :* Coder des fonctions pour calculer des statistiques descriptives sur un jeu de données.

### **Phase 2 : Les Bases du Machine Learning**

1.  **Modèles Fondamentaux :**
    *   *Concepts :* Régression Linéaire, Régression Logistique.
    *   *Projet Pratique :* Implémenter ces deux modèles from scratch, y compris la descente de gradient pour l'entraînement.
2.  **Principes de l'Entraînement :**
    *   *Concepts :* Fonction de coût (Loss function), sur-apprentissage (overfitting), régularisation (L1, L2), ensembles de données (entraînement, validation, test).
    *   *Projet Pratique :* Ajouter la régularisation à vos modèles précédents et créer un script qui divise un dataset.

### **Phase 3 : Le Deep Learning en Profondeur**

1.  **Réseaux de Neurones (from scratch) :**
    *   *Concepts :* Perceptron, Perceptron Multi-Couches (MLP), fonctions d'activation (Sigmoid, ReLU), Forward Propagation.
    *   *Projet Pratique :* Coder un MLP pour un problème de classification simple (ex: sur le dataset Iris ou MNIST).
2.  **L'Entraînement des Réseaux Profonds :**
    *   *Concepts :* Backpropagation (rétropropagation du gradient), optimiseurs (SGD, Adam).
    *   *Projet Pratique :* Implémenter l'algorithme de backpropagation pour votre MLP.
3.  **Traitement de Séquences (Avant le Transformer) :**
    *   *Concepts :* Réseaux de Neurones Récurrents (RNN), LSTMs. Comprendre le problème du "vanishing/exploding gradient".
    *   *Projet Pratique :* Coder un RNN simple pour une tâche de prédiction de séquence.

### **Phase 4 : Vers les Modèles Génératifs (Votre Objectif)**

1.  **Embeddings (Plongements Lexicaux) :**
    *   *Concepts :* One-hot encoding, Word2Vec (Skip-gram, CBOW), GloVe. L'idée de représenter des mots dans un espace vectoriel dense.
    *   *Projet Pratique :* Implémenter un modèle Word2Vec simple from scratch.
2.  **Le Mécanisme d'Attention :**
    *   *Concepts :* Comprendre l'attention comme un moyen de pondérer l'importance des inputs. D'abord avec les RNNs (Bahdanau, Luong attention).
    *   *Projet Pratique :* Ajouter un mécanisme d'attention à votre RNN précédent.
3.  **L'Architecture Transformer :**
    *   *Concepts :* **Self-Attention**, Multi-Head Attention, Positional Encodings, architecture Encodeur-Décodeur. Lire le papier "Attention Is All You Need".
    *   *Projet Pratique :* Coder un bloc Transformer (Self-Attention + Feed Forward) from scratch.
4.  **Modèles de Langage (LLM) :**
    *   *Concepts :* Architecture de type GPT (décodeur-seulement), génération de texte (greedy search, beam search), fine-tuning.
    *   *Projet Pratique :* Assembler vos blocs Transformer pour créer un mini-GPT capable de générer du texte caractère par caractère ou mot par mot.
