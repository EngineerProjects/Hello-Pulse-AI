"""
Classe de base pour le chargement des prompts

Cette classe gère la logique commune de :
- Définition du répertoire des prompts
- Chargement des fichiers .txt
- Mise en cache en mémoire
"""
from pathlib import Path
from typing import Dict


class BasePromptLoader:
    """Classe de base pour charger les prompts depuis des fichiers .txt"""
    
    def __init__(self, prompts_dir: Path = None):
        """
        Initialise le loader.
        
        Args:
            prompts_dir: Chemin vers le répertoire des prompts.
                         Si None, utilise le répertoire du fichier enfant.
        """
        if prompts_dir is None:
            # Cette astuce ne fonctionne que si la classe enfant 
            # est dans son propre dossier de prompts
            # Ce qui est le cas pour assistant, facilitator, et general
            raise ValueError("prompts_dir must be provided by the child class")
        
        self.prompts_dir = prompts_dir
        self._prompts_cache: Dict[str, str] = {}

    def load_prompt(self, filename: str) -> str:
        """
        Charge un prompt depuis un fichier avec mise en cache.
        
        Args:
            filename: Nom du fichier à charger (relatif à prompts_dir)
            
        Returns:
            Contenu du fichier prompt
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
        """
        if filename in self._prompts_cache:
            return self._prompts_cache[filename]
        
        file_path = self.prompts_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(
                f"Fichier de prompt non trouvé: {file_path}"
            )
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._prompts_cache[filename] = content
        return content
    
    def clear_cache(self) -> None:
        """Vide le cache des prompts (utile pour les tests)"""
        self._prompts_cache.clear()