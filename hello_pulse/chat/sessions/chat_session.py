"""
Gestion des sessions de chat génériques avec n'importe quel agent
"""
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
from pathlib import Path
import httpx
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, ToolCallPart, ToolReturnPart
from pydantic_ai.agent import capture_run_messages

from hello_pulse.models.schemas import PostureType, AgentResponse
from hello_pulse.data_providers.base_provider import BaseDataProvider
from hello_pulse.chat.utils import SessionLogger, ToolCall
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
    Cette classe est découplée des agents spécifiques et utilise le pattern
    de data provider pour récupérer les données de session.
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
        
        # Nom de l'agent pour référence
        self.agent_name = getattr(agent, 'name', 'unknown_agent')
        
        # Historique des messages pour Pydantic AI (format ModelMessage)
        self.pydantic_messages: List[ModelMessage] = []
        
        # Logger de session
        self.logger = SessionLogger(
            session_id=session_id,
            agent_name=self.agent_name
        )
    
    # --- MÉTHODES __aenter__ ET __aexit__ SUPPRIMÉES ---
    # La gestion du http_client se fait via lazy initialization
    # et la méthode cleanup()
    
    async def send_message(self, user_message: str) -> Any:
        """
        Envoie un message à l'agent et obtient une réponse.
        CORRECTIONS APPLIQUÉES :
        - Gère le cycle de vie MCP avec `async with`
        - ✅ CORRECTION: Gère intelligemment le type de sortie 
        - (GeneralOutput, AgentResponse, ou str) pour un affichage propre.
        """
        # Initialiser le http_client si nécessaire (lazy initialization)
        if not self.http_client:
            self.http_client = httpx.AsyncClient()
        
        # Ajouter le message de l'utilisateur à l'historique
        user_msg = ChatMessage(
            role='user',
            content=user_message,
            agent_name=self.agent_name
        )
        self.history.append(user_msg)
        
        # Logger le message utilisateur
        self.logger.log_message(role='user', content=user_message)

        # Créer les dépendances pour l'agent via la factory
        deps = await self.agent_deps_factory(
            data_provider=self.data_provider,
            http_client=self.http_client
        )
        
        # Capturer les messages échangés avec l'agent (pour les tool calls)
        with capture_run_messages() as captured_messages:
            
            # Le contexte `async with` est OBLIGATOIRE pour les MCP servers
            async with self.agent:
                result = await self.agent.run(
                    user_message, 
                    deps=deps,
                    message_history=self.pydantic_messages
                )
        
        # Extraire les tools appelés et afficher les liens de recherche
        tool_calls_list = self._process_tool_calls(captured_messages)
        
        # Mettre à jour l'historique Pydantic AI avec les nouveaux messages
        self.pydantic_messages.extend(result.new_messages())
        
        # Extraire la réponse (différent selon le type d'agent)
        response_output = result.output
        
        # --- ⬇️ DÉBUT DE LA CORRECTION "RÉPONSE BIZARRE" ⬇️ ---
        
        response_data = None
        
        if isinstance(response_output, GeneralOutput):
            # Pour l'agent General, le 'result' EST le message pour l'utilisateur
            response_text = response_output.result
            response_data = response_output.model_dump()
            
        elif hasattr(response_output, 'message'):
            # Pour l'agent Facilitator (AgentResponse)
            response_text = response_output.message
            if hasattr(response_output, 'model_dump'):
                response_data = response_output.model_dump()
                
        elif isinstance(response_output, str):
            # Pour l'agent Assistant (output_type=str)
            response_text = response_output
            
        else:
            # Fallback (ce qui causait l'erreur)
            response_text = str(response_output)
        
        # S'assurer que response_data est peuplé si c'est un pydantic model
        if response_data is None and hasattr(response_output, 'model_dump'):
            response_data = response_output.model_dump()
            
        # --- ⬆️ FIN DE LA CORRECTION ⬆️ ---
        
        # Ajouter la réponse de l'agent à l'historique
        agent_msg = ChatMessage(
            role='agent',
            content=response_text,
            agent_name=self.agent_name,
            response_data=response_data
        )
        self.history.append(agent_msg)
        
        # Logger la réponse de l'agent avec les tools appelés
        self.logger.log_message(
            role='agent',
            content=response_text,
            tool_calls=tool_calls_list,
            metadata=response_data 
        )
        
        return response_output
    
    async def chat(self, user_message: str) -> Any:
        """
        Alias pour send_message() - pour compatibilité avec le CLI.
        Args:
            user_message: Le message de l'utilisateur
            
        Returns:
            La réponse de l'agent
        """
        return await self.send_message(user_message)
    
    def _process_tool_calls(self, captured_messages: List[ModelMessage]) -> List[ToolCall]:
        """
        Traite les messages capturés pour extraire les tools appelés.
        Affiche également les liens de recherche dans le terminal.
        Args:
            captured_messages: Messages capturés par capture_run_messages()
            
        Returns:
            Liste des ToolCall pour le logging
        """
        tool_calls_list = []
        search_links = []
        
        for msg in captured_messages:
            # Rechercher les tool calls dans les ModelResponse
            if isinstance(msg, ModelResponse):
                for part in msg.parts:
                    if isinstance(part, ToolCallPart):
                        # Créer un ToolCall pour le logging
                        tool_call = ToolCall(
                            tool_name=part.tool_name,
                            arguments=part.args
                        )
                        tool_calls_list.append(tool_call)
                        # Si c'est un tool de recherche web (Tavily), extraire les liens
                        if part.tool_name in ['tavily_search', 'web_search', 'brave_search']:
                            # Les liens seront dans le résultat du tool
                            # On les affichera après avoir trouvé le ToolReturnPart correspondant
                            pass
            
            # Rechercher les résultats de tools dans les ModelRequest
            elif isinstance(msg, ModelRequest):
                for part in msg.parts:
                    if isinstance(part, ToolReturnPart):
                        # Trouver le ToolCall correspondant
                        for tc in tool_calls_list:
                            if tc.tool_name and not tc.result:
                                tc.result = str(part.content)[:500]  # Limiter à 500 chars
                                
                                # Extraire les liens si c'est un tool de recherche
                                if tc.tool_name in ['tavily_search', 'web_search', 'brave_search']:
                                    links = self._extract_search_links(part.content)
                                    search_links.extend(links)
                                    
                                break
        
        # Afficher les liens de recherche AVANT la réponse de l'agent
        if search_links:
            print(f"\n{'='*60}")
            print(f"🔍 SOURCES UTILISÉES PAR L'AGENT:")
            print(f"{'='*60}")
            for i, link in enumerate(search_links, 1):
                print(f"  [{i}] {link}")
            print(f"{'='*60}\n")
        
        return tool_calls_list
    
    def _extract_search_links(self, tool_result: Any) -> List[str]:
        """
        Extrait les liens depuis le résultat d'un tool de recherche.
        Args:
            tool_result: Résultat du tool (peut être dict, str, ou autre)
            
        Returns:
            Liste des URLs trouvées
        """
        links = []
        
        try:
            # Si c'est déjà un dict
            if isinstance(tool_result, dict):
                # Format Tavily : {'results': [{'url': '...', 'title': '...'}]}
                if 'results' in tool_result:
                    for result in tool_result['results']:
                        if 'url' in result:
                            links.append(result['url'])
                
                # Format alternatif : {'urls': [...]}
                elif 'urls' in tool_result:
                    links.extend(tool_result['urls'])
            
            # Si c'est une string JSON
            elif isinstance(tool_result, str):
                try:
                    data = json.loads(tool_result)
                    return self._extract_search_links(data)
                except json.JSONDecodeError:
                    # Pas du JSON, chercher des URLs avec regex
                    import re
                    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+?(?=[\s\)\]\}]|$)'
                    links = re.findall(url_pattern, tool_result)
        
        except Exception as e:
            # En cas d'erreur, ignorer silencieusement
            pass
        
        return links[:10]  # Limiter à 10 liens max
    
    def get_history(self) -> List[ChatMessage]:
        """Retourne l'historique complet de la conversation"""
        return self.history
    
    def clear_history(self):
        """Efface l'historique de la conversation"""
        self.history = []
        print("🗑️  Historique effacé")
    
    def print_history(self, last_n: Optional[int] = None):
        """Affiche l'historique de conversation"""
        messages = self.history[-last_n:] if last_n else self.history
        
        print("\n" + "="*60)
        print(f"📜 HISTORIQUE ({len(messages)} messages)")
        print("="*60 + "\n")
        
        for msg in messages:
            icon = "👤" if msg.role == "user" else "🤖"
            timestamp = msg.timestamp.strftime("%H:%M:%S")
            print(f"{icon} [{timestamp}] {msg.role.upper()}")
            print(f"   {msg.content}")
            print()
    
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
            'log_file': str(self.logger.get_log_path())
        }
    
    def get_log_path(self) -> Path:
        """
        Retourne le chemin du fichier de logs de la session.
        Returns:
            Path vers le fichier de logs
        """
        return self.logger.get_log_path()
    
    async def cleanup(self):
        """Nettoie les ressources (ferme le http_client si nécessaire)"""
        if self.http_client:
            await self.http_client.aclose()
            self.http_client = None