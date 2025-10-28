"""
Handler de base pour les agents - classe abstraite
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseAgentHandler(ABC):
    """
    Classe abstraite pour les handlers d'agents.
    Chaque agent doit implémenter son propre handler avec ses commandes spécifiques.
    """
    
    def __init__(self, session):
        """
        Args:
            session: Instance de la session de chat de l'agent (ex: AssistantChatSession)
        """
        self.session = session
    
    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Retourne le nom de l'agent"""
        pass
    
    @property
    @abstractmethod
    def agent_emoji(self) -> str:
        """Retourne l'emoji de l'agent"""
        pass
    
    @abstractmethod
    def get_available_commands(self) -> Dict[str, str]:
        """
        Retourne un dictionnaire des commandes spécifiques à l'agent.
        Returns:
            Dict[command, description]
        """
        pass
    
    @abstractmethod
    async def handle_command(self, command: str) -> bool:
        """
        Traite une commande spécifique à l'agent.
        Args:
            command: La commande à traiter (ex: '/posture', '/phase')
            
        Returns:
            True si la commande a été traitée, False sinon
        """
        pass
    
    @abstractmethod
    async def display_context(self):
        """Affiche le contexte spécifique de l'agent"""
        pass
    
    def get_session_info(self) -> Dict[str, Any]:
        """
        Retourne les informations générales de la session.
        Returns:
            Dictionnaire avec les infos de session
        """
        return {
            'session_id': self.session.session_id,
            'agent_name': self.agent_name,
            'history_count': len(self.session.history)
        }