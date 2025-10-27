"""
Session de chat spécialisée pour l'agent facilitateur.

Cette classe étend ChatSession avec des fonctionnalités spécifiques
au facilitateur comme la gestion des postures et l'accès au contexte.
"""
from typing import Optional
from hello_pulse.chat.sessions.chat_session import ChatSession
from hello_pulse.models.schemas import PostureType, SessionContext
from hello_pulse.agents.facilitator.dependencies import FacilitatorDeps


class FacilitatorChatSession(ChatSession):
    """
    Session de chat spécialisée pour le facilitateur.
    
    Ajoute des méthodes pour :
    - Changer la posture de l'agent
    - Accéder au contexte de session
    - Accéder à la posture actuelle
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_posture = PostureType.GUIDE
        self._cached_context: Optional[SessionContext] = None
    
    @property
    def current_posture(self) -> PostureType:
        """Retourne la posture actuelle de l'agent"""
        return self._current_posture
    
    async def change_posture(self, new_posture: PostureType):
        """
        Change la posture de l'agent facilitateur.
        
        Args:
            new_posture: Nouvelle posture à adopter
        """
        self._current_posture = new_posture
        print(f"✅ Posture changée : {new_posture.value}")
    
    async def get_session_context(self) -> SessionContext:
        """
        Récupère le contexte actuel de la session depuis le data provider.
        
        Returns:
            SessionContext avec toutes les informations
        """
        self._cached_context = await self.data_provider.get_session_context()
        return self._cached_context
    
    @property
    def session_context(self) -> Optional[SessionContext]:
        """
        Retourne le contexte de session en cache.
        
        Note: Appeler get_session_context() pour rafraîchir
        """
        return self._cached_context
    
    async def send_message(self, user_message: str):
        """
        Override pour rafraîchir le contexte avant chaque message.
        """
        # Rafraîchir le contexte avant d'envoyer le message
        await self.get_session_context()
        
        # Appeler la méthode parente
        return await super().send_message(user_message)
