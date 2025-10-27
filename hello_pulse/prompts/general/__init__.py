"""
Gestionnaire de prompts pour l'Agent General
"""
from pathlib import Path


class GeneralPrompts:
    """
    Gestionnaire des prompts système pour l'agent general.
    
    Charge les instructions depuis des fichiers texte pour
    faciliter les modifications sans toucher au code.
    """
    
    def __init__(self):
        self.prompts_dir = Path(__file__).parent
    
    def get_base_instructions(self) -> str:
        """
        Charge les instructions de base depuis instructions.txt
        
        Returns:
            Contenu du fichier instructions.txt
        """
        instructions_file = self.prompts_dir / 'instructions.txt'
        
        if not instructions_file.exists():
            return self._get_default_instructions()
        
        with open(instructions_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _get_default_instructions(self) -> str:
        """
        Instructions par défaut si le fichier n'existe pas
        
        Returns:
            Instructions de base en fallback
        """
        return """
Tu es un Agent General autonome et polyvalent.

RÔLE :
Tu es capable de travailler sur des tâches complexes nécessitant
plusieurs étapes, recherches approfondies et utilisation de multiples tools.

CAPACITÉS :
- Recherche web approfondie et analyse de sources multiples
- Navigation et interaction avec des sites web
- Création, lecture et modification de fichiers et documents
- Exécution de commandes et scripts si nécessaire
- Et tous les autres tools MCP à ta disposition

WORKFLOW RECOMMANDÉ :
1. 📋 ANALYSE : Comprends bien la tâche et ses objectifs
2. 🎯 PLANIFICATION : Décompose en sous-tâches concrètes
3. 🔧 EXÉCUTION : Utilise les tools nécessaires étape par étape
4. ✅ VÉRIFICATION : Évalue si chaque étape est réussie
5. 🎉 CONCLUSION : Détermine si l'objectif global est atteint

IMPORTANT :
- Sois méthodique et structuré dans ton approche
- Utilise TOUS les tools dont tu as besoin sans limitation
- Raisonne à voix haute pour expliquer tes actions
- Évalue honnêtement si l'objectif est atteint
- Si non atteint, propose des prochaines étapes claires
"""