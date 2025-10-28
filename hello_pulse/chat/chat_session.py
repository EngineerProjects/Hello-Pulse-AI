"""
Gestion des sessions de chat génériques avec n'importe quel agent
"""
import asyncio
from typing import List, Optional, Dict, Any, AsyncGenerator
from datetime import datetime
import json
from pathlib import Path
import httpx
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, ToolCallPart, ToolReturnPart
from pydantic_ai.agent import capture_run_messages, AgentStreamEvent

from hello_pulse.models.schemas import PostureType, AgentResponse
from hello_pulse.data_providers.base_provider import BaseDataProvider

from hello_pulse.agents.general.output import GeneralOutput


class ChatMessage:
    """Message dans l'historique du chat"""
    def __init__(
        self, 
        role: str,  # 'user' ou 'agent'
        content: str,
        agent_name: Optional[str] = None,
        response_data: Optional[dict] = None,
        timestamp: Optional[datetime] = None
    ):
        self.role = role
        self.content = content
        self.agent_name = agent_name
        self.response_data = response_data
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le message en dictionnaire"""
        data = {
            'role': self.role,
            'content': self.content,
            'agent_name': self.agent_name,
            'timestamp': self.timestamp.isoformat()
        }
        if self.response_data:
            data['response_data'] = self.response_data
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ChatMessage':
        """Crée un message depuis un dictionnaire"""
        return cls(
            role=data['role'],
            content=data['content'],
            agent_name=data.get('agent_name'),
            response_data=data.get('response_data'),
            timestamp=datetime.fromisoformat(data['timestamp'])
        )


class ChatSession:
    """
    Session de chat GÉNÉRIQUE - fonctionne avec n'importe quel agent Pydantic AI.
    Cette classe est le "coeur" de la logique de session.
    Elle gère l'historique des messages et l'appel à l'agent.
    """
    
    def __init__(
        self,
        agent: Agent,
        agent_deps_factory,  # Callable qui crée les dépendances de l'agent
        data_provider: BaseDataProvider,
        session_id: str = "default-session"
    ):
        """
        Args:
            agent: Instance d'agent Pydantic AI (facilitator, general, etc.)
            agent_deps_factory: Fonction qui crée les dépendances de l'agent
            data_provider: Fournisseur de données (Mock ou API)
            session_id: ID unique de la session
        """
        self.agent = agent
        self.agent_deps_factory = agent_deps_factory
        self.data_provider = data_provider
        self.session_id = session_id
        self.history: List[ChatMessage] = []
        self.http_client: Optional[httpx.AsyncClient] = None
        
        self.agent_name = getattr(agent, 'name', 'unknown_agent')
        self.pydantic_messages: List[ModelMessage] = []
        
        # Le logger a été retiré. Le CLI (terminal_app) s'en chargera.
        # self.logger = SessionLogger(...) 
    
    async def _get_http_client(self) -> httpx.AsyncClient:
        """Crée le client HTTP si nécessaire (lazy initialization)"""
        if self.http_client is None:
            self.http_client = httpx.AsyncClient()
        return self.http_client

    # send_message() et chat() sont remplacés par stream_chat()

    async def stream_chat(self, user_message: str) -> AsyncGenerator[AgentStreamEvent, None]:
        """
        Envoie un message à l'agent et streame les événements ReAct (non bloquant).
        
        Args:
            user_message: Le message de l'utilisateur
            
        Yields:
            AgentStreamEvent: Événements de streaming 
                              (ex: 'text_delta', 'tool_call', 'tool_output', 'end', 'error')
        """
        
        # 1. Préparer le message et les dépendances
        http_client = await self._get_http_client()
        
        user_msg = ChatMessage(
            role='user',
            content=user_message,
            agent_name=self.agent_name
        )
        self.history.append(user_msg)

        # Créer les dépendances pour l'agent via la factory
        deps = await self.agent_deps_factory(
            data_provider=self.data_provider,
            http_client=http_client
        )
        
        # 2. Lancer le streaming
        # Le contexte `async with` est OBLIGATOIRE pour les MCP servers
        final_output = None
        run_result = None
        try:
            async with self.agent:
                # Utilise run_stream_events au lieu de run
                async for event in self.agent.run_stream_events(
                    user_message, 
                    deps=deps,
                    message_history=self.pydantic_messages
                ):
                    if event.name == 'end':
                        # L'événement 'end' contient le résultat final
                        run_result = event.run_result
                        final_output = run_result.output
                        
                        # Mettre à jour l'historique Pydantic AI 
                        # pour le prochain tour
                        self.pydantic_messages.extend(run_result.new_messages())
                    
                    # Transmettre l'événement au consommateur (le CLI)
                    yield event
        
        except Exception as e:
            # Gérer les erreurs de streaming et les transmettre
            error_data = {"error_message": str(e), "type": type(e).__name__}
            yield AgentStreamEvent(
                name='error', 
                data=error_data
            )
            # Afficher le traceback complet côté serveur (coeur) pour le débogage
            import traceback
            traceback.print_exc()
            return

        # 3. Post-traitement (après la fin du stream)
        if final_output:
            # Extraire le contenu textuel de la réponse finale
            response_text = self._extract_text_from_output(final_output)
            
            # Extraire les données de réponse structurées
            response_data = None
            if hasattr(final_output, 'model_dump'):
                response_data = final_output.model_dump()
            
            # Ajouter la réponse finale de l'agent à l'historique
            agent_msg = ChatMessage(
                role='agent',
                content=response_text,
                agent_name=self.agent_name,
                response_data=response_data
            )
            self.history.append(agent_msg)
            
    def _extract_text_from_output(self, response_output: Any) -> str:
        """Extrait le message textuel de la sortie finale de l'agent."""
        
        if isinstance(response_output, GeneralOutput):
            # Pour l'agent General, le 'result' EST le message
            return response_output.result
            
        elif hasattr(response_output, 'message'):
            # Pour l'agent Facilitator (AgentResponse)
            return response_output.message
                 
        elif isinstance(response_output, str):
            # Pour l'agent Assistant (output_type=str)
            return response_output
            
        else:
            # Fallback
            return str(response_output)
    
    def get_history(self) -> List[ChatMessage]:
        """Retourne l'historique complet de la conversation"""
        return self.history
    
    def clear_history(self):
        """Efface l'historique de la conversation"""
        self.history = []
        self.pydantic_messages = []
        # Le print() est géré par le CLI
    
    def print_history(self, last_n: Optional[int] = None):
        """(Obsolète) - Cette logique est maintenant dans terminal_app/app.py"""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne des statistiques sur la session"""
        agent_messages = [m for m in self.history if m.role == 'agent']
        user_messages = [m for m in self.history if m.role == 'user']
        
        return {
            'session_id': self.session_id,
            'agent_name': self.agent_name,
            'total_messages': len(self.history),
            'user_messages': len(user_messages),
            'agent_messages': len(agent_messages),
        }
    
    def get_log_path(self) -> Path:
        """(Obsolète) - Le logger est géré par terminal_app/cli_utils/logger.py"""
        # La session CLI (SessionManager) gérera le logger
        raise NotImplementedError("Logging is handled by terminal_app")
    
    async def cleanup(self):
        """Nettoie les ressources (ferme le http_client si nécessaire)"""
        if self.http_client:
            await self.http_client.aclose()
            self.http_client = None