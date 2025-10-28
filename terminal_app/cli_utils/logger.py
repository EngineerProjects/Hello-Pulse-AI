"""
Système de logging pour les sessions de chat Hello Pulse

Ce module fournit un logger structuré qui enregistre :
- L'historique complet des messages (user + agent)
- Les tools appelés et leurs résultats
- Les métadonnées de chaque session
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ToolCall:
    """Représente un appel de tool par l'agent"""
    tool_name: str
    arguments: Dict[str, Any]
    result: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            'tool_name': self.tool_name,
            'arguments': self.arguments,
            'result': self.result,
            'timestamp': self.timestamp.isoformat(),
            'error': self.error
        }


@dataclass
class LogEntry:
    """Entrée de log pour un message"""
    role: str  # 'user' ou 'agent'
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    tool_calls: List[ToolCall] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'tool_calls': [tc.to_dict() for tc in self.tool_calls],
            'metadata': self.metadata
        }


class SessionLogger:
    """
    Logger pour une session de chat
    
    Enregistre tous les échanges, tools appelés et métadonnées
    dans un fichier JSON structuré.
    """
    
    def __init__(self, session_id: str, agent_name: str, log_dir: Optional[Path] = None):
        """
        Args:
            session_id: ID unique de la session
            agent_name: Nom de l'agent
            log_dir: Dossier où sauvegarder les logs (défaut: logs/ à la racine)
        """
        self.session_id = session_id
        self.agent_name = agent_name
        
        # Déterminer le dossier de logs
        if log_dir is None:
            # Par défaut : logs/ à la racine du projet
            # Le chemin est relatif à CE fichier (terminal_app/cli_utils/logger.py)
            project_root = Path(__file__).parent.parent.parent
            self.log_dir = project_root / "logs"
        else:
            self.log_dir = log_dir
        
        self.log_dir.mkdir(exist_ok=True)
        
        # Créer un fichier de log unique pour cette session
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_file = self.log_dir / f"{agent_name}_{session_id}_{timestamp}.json"
        
        # Initialiser la structure des logs
        self.logs: List[LogEntry] = []
        self.session_metadata = {
            'session_id': session_id,
            'agent_name': agent_name,
            'started_at': datetime.now().isoformat(),
            'total_messages': 0,
            'total_tool_calls': 0
        }
        
        # Sauvegarder les métadonnées initiales
        self._save()
    
    def log_message(
        self, 
        role: str, 
        content: str, 
        tool_calls: Optional[List[ToolCall]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Enregistre un message dans les logs
        
        Args:
            role: 'user' ou 'agent'
            content: Contenu du message
            tool_calls: Liste des tools appelés (si agent)
            metadata: Métadonnées additionnelles
        """
        entry = LogEntry(
            role=role,
            content=content,
            tool_calls=tool_calls or [],
            metadata=metadata or {}
        )
        self.logs.append(entry)
        
        # Mettre à jour les métadonnées
        self.session_metadata['total_messages'] += 1
        self.session_metadata['total_tool_calls'] += len(tool_calls or [])
        self.session_metadata['last_updated'] = datetime.now().isoformat()
        
        # Sauvegarder après chaque message
        self._save()
    
    def log_tool_call(
        self, 
        tool_name: str, 
        arguments: Dict[str, Any],
        result: Optional[str] = None,
        error: Optional[str] = None
    ) -> ToolCall:
        """
        Crée un objet ToolCall pour logger
        
        Args:
            tool_name: Nom du tool
            arguments: Arguments passés au tool
            result: Résultat du tool
            error: Message d'erreur si échec
            
        Returns:
            Instance de ToolCall
        """
        return ToolCall(
            tool_name=tool_name,
            arguments=arguments,
            result=result,
            error=error
        )
    
    def _save(self):
        """Sauvegarde les logs dans le fichier JSON"""
        log_data = {
            'metadata': self.session_metadata,
            'logs': [entry.to_dict() for entry in self.logs]
        }
        
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du logger: {e}")
    
    def get_log_path(self) -> Path:
        """Retourne le chemin du fichier de log"""
        return self.log_file
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de la session"""
        return {
            **self.session_metadata,
            'log_file': str(self.log_file)
        }
    
    @classmethod
    def load_logs(cls, log_file: Path) -> Dict[str, Any]:
        """
        Charge les logs depuis un fichier
        
        Args:
            log_file: Chemin vers le fichier de logs
            
        Returns:
            Dictionnaire avec metadata et logs
        """
        with open(log_file, 'r', encoding='utf-8') as f:
            return json.load(f)