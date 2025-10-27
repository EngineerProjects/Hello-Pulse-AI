"""
Gestionnaire de prompts pour l'Agent General
"""
from pathlib import Path
from hello_pulse.prompts.base_loader import BasePromptLoader


class GeneralPrompts(BasePromptLoader):
    """
    Charge et gère les prompts de l'agent general.
    Hérite de BasePromptLoader pour la logique de chargement.
    """
    
    def __init__(self, prompts_dir: Path = None):
        """
        Initialise le gestionnaire de prompts.
        """
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent
        super().__init__(prompts_dir=prompts_dir)
    
    def get_base_instructions(self) -> str:
        """
        Récupère les instructions de base de l'agent general.
        
        Returns:
            Instructions complètes pour l'agent general
        """
        return self.load_prompt('instructions.txt')