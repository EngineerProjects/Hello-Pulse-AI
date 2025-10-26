"""
Gestionnaire de prompts pour l'agent facilitateur
"""
from pathlib import Path
from typing import Dict


class FacilitatorPrompts:
    """Charge et gère les prompts de l'agent facilitateur"""
    
    def __init__(self, prompts_dir: Path = None):
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent
        self.prompts_dir = prompts_dir
        self._prompts_cache: Dict[str, str] = {}
    
    def load_prompt(self, filename: str) -> str:
        """Charge un prompt depuis un fichier"""
        if filename in self._prompts_cache:
            return self._prompts_cache[filename]
        
        file_path = self.prompts_dir / filename
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._prompts_cache[filename] = content
        return content
    
    def get_base_instructions(self) -> str:
        """Instructions de base de l'agent"""
        return self.load_prompt('base_instructions.txt')
    
    def get_posture_prompt(self, posture: str) -> str:
        """Prompt spécifique à une posture"""
        return self.load_prompt(f'postures/{posture}.txt')