"""
Gestionnaire de prompts pour l'agent facilitateur
"""
from pathlib import Path
from hello_pulse.prompts.base_loader import BasePromptLoader


class FacilitatorPrompts(BasePromptLoader):
    """
    Charge et gère les prompts de l'agent facilitateur.
    Hérite de BasePromptLoader pour la logique de chargement.
    """
    
    def __init__(self, prompts_dir: Path = None):
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent
        super().__init__(prompts_dir=prompts_dir)
    
    def get_base_instructions(self) -> str:
        """Instructions de base de l'agent"""
        return self.load_prompt('base_instructions.txt')
    
    def get_posture_prompt(self, posture: str) -> str:
        """Prompt spécifique à une posture"""
        # Assure que le nom de fichier est sécurisé
        safe_posture = Path(posture).name
        if not safe_posture.endswith('.txt'):
            safe_posture += '.txt'
            
        return self.load_prompt(f'postures/{safe_posture}')