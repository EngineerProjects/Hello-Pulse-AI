"""
Gestionnaire de prompts pour l'agent assistant
"""
from pathlib import Path
from typing import Dict


class AssistantPrompts:
    """
    Charge et gère les prompts de l'agent assistant.
    
    Contrairement au facilitateur, l'assistant a des prompts plus simples
    car il n'a pas de postures dynamiques.
    """
    
    def __init__(self, prompts_dir: Path = None):
        """
        Initialise le gestionnaire de prompts.
        
        Args:
            prompts_dir: Répertoire contenant les fichiers de prompts.
                        Par défaut, utilise le répertoire du module.
        """
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent
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
                f"Prompt file not found: {file_path}"
            )
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._prompts_cache[filename] = content
        return content
    
    def get_base_instructions(self) -> str:
        """
        Récupère les instructions de base de l'assistant.
        
        Returns:
            Instructions complètes pour l'agent assistant
        """
        return self.load_prompt('instructions.txt')
    
    def clear_cache(self) -> None:
        """Vide le cache des prompts (utile pour les tests)"""
        self._prompts_cache.clear()
