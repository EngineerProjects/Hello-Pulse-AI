"""
Gestionnaire centralisé des sessions pour l'application Terminal.
Ce fichier vit dans terminal_app/
"""
from pathlib import Path
from datetime import datetime
from typing import Optional, Literal
import json

# Imports depuis le COEUR IA (bibliothèque hello_pulse)
from hello_pulse.chat.sessions.session_factory import (
    create_facilitator_session,
    create_assistant_session,
    create_general_session
)
from hello_pulse.chat.chat_session import ChatSession

# Imports depuis le CLI local (application terminal_app)
from terminal_app.agent_handlers import (
    FacilitatorHandler,
    AssistantHandler,
    GeneralHandler
)
from terminal_app.agent_handlers.base_handler import BaseAgentHandler
from terminal_app.cli_utils.logger import SessionLogger

AgentType = Literal['assistant', 'facilitator', 'general']


class SessionManager:
    """Gestion centralisée des sessions pour l'application terminal"""
    
    def __init__(self, sessions_dir: Optional[str] = None):
        """
        Args:
            sessions_dir: Répertoire pour sauvegarder l'historique des sessions
        """
        if sessions_dir is None:
            # Le chemin est relatif à ce fichier (terminal_app/session_manager.py)
            # remonte de deux niveaux (terminal_app -> racine) et cherche 'chat_histories'
            project_root = Path(__file__).parent.parent
            sessions_dir = str(project_root / 'chat_histories')
        
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)
        
        self.current_session: Optional[ChatSession] = None
        self.current_handler: Optional[BaseAgentHandler] = None
        self.current_agent_type: Optional[AgentType] = None
        self.logger: Optional[SessionLogger] = None
    
    def create_session(
        self,
        agent_type: AgentType,
        session_id: Optional[str] = None
    ) -> tuple:
        """
        Crée une nouvelle session pour un agent donné.

        Args:
            agent_type: Type d'agent ('assistant', 'facilitator', 'general')
            session_id: ID personnalisé (optionnel, généré automatiquement sinon)
            
        Returns:
            Tuple (session, handler, logger)
        """
        if session_id is None:
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            session_id = f"{agent_type}-{timestamp}"
        
        # Créer la session selon le type d'agent (depuis le coeur IA)
        if agent_type == 'assistant':
            session = create_assistant_session(session_id=session_id)
            handler = AssistantHandler(session)
        
        elif agent_type == 'facilitator':
            session = create_facilitator_session(session_id=session_id)
            handler = FacilitatorHandler(session)
        
        elif agent_type == 'general':
            session = create_general_session(session_id=session_id)
            handler = GeneralHandler(session)
        
        else:
            raise ValueError(f"Type d'agent inconnu: {agent_type}")
        
        self.current_session = session
        self.current_handler = handler
        self.current_agent_type = agent_type
        
        # Créer le logger du CLI pour cette session
        self.logger = SessionLogger(
            session_id=session.session_id,
            agent_name=session.agent_name,
            log_dir=self.sessions_dir # Utilise le dossier de logs/historiques
        )
        
        return session, handler, self.logger
    
    def switch_agent(self, new_agent_type: AgentType) -> tuple:
        """
        Change d'agent en créant une nouvelle session.
        NOTE : Ne sauvegarde pas l'historique de la session précédente.

        Args:
            new_agent_type: Type du nouvel agent
            
        Returns:
            Tuple (session, handler, logger)
        """
        # (La sauvegarde de session n'était pas implémentée dans l'original)
        # if self.current_session:
        #     self.save_current_session()
        
        return self.create_session(new_agent_type)
    
    async def cleanup_current_session(self):
        """Nettoie la session actuelle (ferme les ressources)"""
        if self.current_session and hasattr(self.current_session, 'cleanup'):
            await self.current_session.cleanup()
        
        self.current_session = None
        self.current_handler = None
        self.current_agent_type = None
        self.logger = None