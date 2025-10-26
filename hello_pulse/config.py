"""
Gestionnaire de configuration centralisé pour Hello Pulse
"""
import yaml
from pathlib import Path
from typing import Any, Optional
from functools import lru_cache


class Config:
    """
    Gestionnaire de configuration singleton.
    
    Charge et donne accès à la configuration globale depuis config.yml
    """
    
    _instance: Optional['Config'] = None
    _config: dict = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Charge la configuration depuis le fichier YAML"""
        config_path = Path(__file__).parent.parent / 'config.yml'
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Récupère une valeur de configuration par son chemin.
        
        Args:
            key_path: Chemin de la clé (ex: "agents.facilitator.model.name")
            default: Valeur par défaut si la clé n'existe pas
            
        Returns:
            La valeur de configuration ou default
        """
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
