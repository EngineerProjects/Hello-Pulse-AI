"""
Gestionnaire centralisé des sessions pour tous les agents
"""
from pathlib import Path
from datetime import datetime
from typing import Optional, Literal
import json
from hello_pulse.chat.sessions.session_factory import (
    create_facilitator_session,
    create_assistant_session
)
from hello_pulse.chat.agent_handlers import (
    FacilitatorHandler,
    AssistantHandler,
    StudioHandler
)

AgentType = Literal['assistant', 'facilitator', 'studio']


class SessionManager:
    """Gestion centralisée des sessions pour tous les agents"""
    
    def __init__(self, sessions_dir: str = None):
        """
        Args:
            sessions_dir: Répertoire pour sauvegarder les sessions
        """
        if sessions_dir is None:
            # Créer le dossier sessions au niveau du module chat
            sessions_dir = str(Path(__file__).parent.parent / 'sessions')
        
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)
        
        self.current_session = None
        self.current_handler = None
        self.current_agent_type = None
    
    def create_session(
        self,
        agent_type: AgentType,
        session_id: Optional[str] = None
    ) -> tuple:
        """
        Crée une nouvelle session pour un agent donné.
        
        Args:
            agent_type: Type d'agent ('assistant', 'facilitator', 'studio')
            session_id: ID personnalisé (optionnel, généré automatiquement sinon)
            
        Returns:
            Tuple (session, handler)
        """
        if session_id is None:
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            session_id = f"{agent_type}-{timestamp}"
        
        # Créer la session selon le type d'agent
        if agent_type == 'assistant':
            session = create_assistant_session(session_id=session_id)
            handler = AssistantHandler(session)
        
        elif agent_type == 'facilitator':
            session = create_facilitator_session(session_id=session_id)
            handler = FacilitatorHandler(session)
        
        elif agent_type == 'studio':
            # Studio pas encore implémenté
            raise NotImplementedError("L'agent Studio n'est pas encore disponible")
        
        else:
            raise ValueError(f"Type d'agent inconnu: {agent_type}")
        
        self.current_session = session
        self.current_handler = handler
        self.current_agent_type = agent_type
        
        return session, handler
    
    def switch_agent(self, new_agent_type: AgentType) -> tuple:
        """
        Change d'agent en créant une nouvelle session.
        
        Args:
            new_agent_type: Type du nouvel agent
            
        Returns:
            Tuple (session, handler)
        """
        if self.current_session:
            # Sauvegarder la session actuelle
            self.save_current_session()
        
        return self.create_session(new_agent_type)
    
    async def cleanup_current_session(self):
        """Nettoie la session actuelle (ferme les ressources)"""
        if self.current_session and hasattr(self.current_session, 'cleanup'):
            await self.current_session.cleanup()
