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

from hello_pulse.models.schemas import PostureType, AgentResponse
from hello_pulse.data_providers.base_provider import BaseDataProvider


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
        session_id: str = "default-session",
        save_history: bool = True
    ):
        """
        Args:
            agent: Instance d'agent Pydantic AI (facilitator, general, etc.)
            agent_deps_factory: Fonction qui crée les dépendances de l'agent
            data_provider: Fournisseur de données (Mock ou API)
            session_id: ID unique de la session
            save_history: Sauvegarder l'historique automatiquement
        """
        self.agent = agent
        self.agent_deps_factory = agent_deps_factory
        self.data_provider = data_provider
        self.session_id = session_id
        self.save_history = save_history
        self.history: List[ChatMessage] = []
        self.http_client: Optional[httpx.AsyncClient] = None
        
        # Chemin pour sauvegarder l'historique
        self.history_dir = Path(__file__).parent.parent.parent / "chat_histories"
        self.history_dir.mkdir(exist_ok=True)
        
        # Nom de l'agent pour référence
        self.agent_name = getattr(agent, 'name', 'unknown_agent')
    
    async def __aenter__(self):
        """Context manager entry"""
        self.http_client = httpx.AsyncClient()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.http_client:
            await self.http_client.aclose()
    
    async def send_message(self, user_message: str) -> Any:
        """
        Envoie un message à l'agent et obtient une réponse.
        
        Args:
            user_message: Le message de l'utilisateur
            
        Returns:
            La réponse de l'agent (type dépend de l'agent)
        """
        if not self.http_client:
            raise RuntimeError("ChatSession must be used as async context manager")
        
        # Ajouter le message de l'utilisateur à l'historique
        user_msg = ChatMessage(
            role='user',
            content=user_message,
            agent_name=self.agent_name
        )
        self.history.append(user_msg)
        
        # Créer les dépendances pour l'agent via la factory
        deps = await self.agent_deps_factory(
            data_provider=self.data_provider,
            http_client=self.http_client
        )
        
        # Appeler l'agent
        result = await self.agent.run(user_message, deps=deps)
        
        # Extraire la réponse (différent selon le type d'agent)
        response_output = result.output
        
        # Convertir la réponse en dict si c'est un BaseModel Pydantic
        response_data = None
        if hasattr(response_output, 'model_dump'):
            response_data = response_output.model_dump()
        
        # Déterminer le message textuel de la réponse
        if hasattr(response_output, 'message'):
            response_text = response_output.message
        elif isinstance(response_output, str):
            response_text = response_output
        else:
            response_text = str(response_output)
        
        # Ajouter la réponse de l'agent à l'historique
        agent_msg = ChatMessage(
            role='agent',
            content=response_text,
            agent_name=self.agent_name,
            response_data=response_data
        )
        self.history.append(agent_msg)
        
        # Sauvegarder l'historique si activé
        if self.save_history:
            self._save_history()
        
        return response_output
    
    def get_history(self) -> List[ChatMessage]:
        """Retourne l'historique complet de la conversation"""
        return self.history
    
    def clear_history(self):
        """Efface l'historique de la conversation"""
        self.history = []
        print("🗑️  Historique effacé")
    
    def _save_history(self):
        """Sauvegarde l'historique dans un fichier JSON"""
        history_file = self.history_dir / f"{self.session_id}.json"
        
        history_data = {
            'session_id': self.session_id,
            'agent_name': self.agent_name,
            'messages': [msg.to_dict() for msg in self.history],
            'last_updated': datetime.now().isoformat()
        }
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
    
    def load_history(self):
        """Charge l'historique depuis un fichier JSON"""
        history_file = self.history_dir / f"{self.session_id}.json"
        
        if not history_file.exists():
            print(f"⚠️  Aucun historique trouvé pour {self.session_id}")
            return
        
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
        
        self.history = [
            ChatMessage.from_dict(msg) 
            for msg in history_data['messages']
        ]
        
        print(f"📂 Historique chargé : {len(self.history)} messages")
    
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
            'agent_messages': len(agent_messages)
        }
