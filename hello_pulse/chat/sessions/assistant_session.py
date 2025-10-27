"""
Session de chat spécialisée pour l'agent assistant.

Cette classe étend ChatSession avec des fonctionnalités spécifiques
à l'assistant comme la gestion du contexte utilisateur.
"""
from typing import Optional
from hello_pulse.chat.sessions.chat_session import ChatSession


class AssistantChatSession(ChatSession):
    """
    Session de chat spécialisée pour l'assistant.
    
    L'assistant est plus simple que le facilitateur :
    - Pas de postures dynamiques
    - Contexte utilisateur (phase, rôle)
    - Mode réactif pur
    """
    
    def __init__(self, *args, user_id: str = "user", user_role: str = "participant", **kwargs):
        super().__init__(*args, **kwargs)
        self._user_id = user_id
        self._user_role = user_role
        self._session_phase = "divergence"
    
    @property
    def user_id(self) -> str:
        """Retourne l'ID de l'utilisateur"""
        return self._user_id
    
    @property
    def user_role(self) -> str:
        """Retourne le rôle de l'utilisateur"""
        return self._user_role
    
    @property
    def session_phase(self) -> str:
        """Retourne la phase actuelle de la session"""
        return self._session_phase
    
    def set_phase(self, phase: str):
        """
        Change la phase de la session.
        
        Args:
            phase: Nouvelle phase (divergence, convergence, priorisation, etc.)
        """
        self._session_phase = phase
        print(f"✅ Phase changée : {phase}")
    
    def set_user_role(self, role: str):
        """
        Change le rôle de l'utilisateur.
        
        Args:
            role: Nouveau rôle (participant, facilitateur, observateur, etc.)
        """
        self._user_role = role
        print(f"✅ Rôle changé : {role}")
    
    def get_context_info(self) -> dict:
        """
        Retourne les informations de contexte pour l'affichage.
        
        Returns:
            Dictionnaire avec le contexte actuel
        """
        return {
            'session_id': self.session_id,
            'user_id': self._user_id,
            'user_role': self._user_role,
            'session_phase': self._session_phase,
            'agent_name': self.agent_name
        }
