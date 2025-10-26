"""
Chargeur de configuration MCP depuis JSON

Charge les serveurs MCP depuis mcp_config.json (format standard MCP)
Compatible avec Claude Desktop, Cline, et autres clients MCP.

Ce module est le chargeur OFFICIEL et UNIQUE pour MCP dans Hello Pulse.
"""
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional
from pydantic_ai.mcp import MCPServerStdio


class MCPConfigLoader:
    """
    Charge les serveurs MCP depuis mcp_config.json (format standard MCP).
    
    Compatible avec le format de configuration de Claude Desktop et autres clients MCP.
    Peut lire le chemin du fichier depuis config.yml pour une configuration centralisée.
    
    Format du fichier mcp_config.json:
    ```json
    {
      "mcpServers": {
        "server_name": {
          "command": "python",
          "args": ["-m", "mcp_server_module"],
          "env": {
            "API_KEY": "${API_KEY}"
          }
        }
      }
    }
    ```
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialise le loader.
        
        Args:
            config_path: Chemin vers mcp_config.json (optionnel)
                        Par défaut: lit depuis config.yml ou cherche à la racine
        """
        self.config_path = self._resolve_config_path(config_path)
        self._config = self._load_config()
        self._mcp_enabled = self._check_if_enabled()
    
    def _resolve_config_path(self, config_path: Optional[str]) -> Path:
        """Résout le chemin du fichier de configuration MCP"""
        if config_path:
            return Path(config_path)
        
        # Essayer de lire depuis config.yml
        try:
            from hello_pulse.config import Config
            yaml_config = Config()
            
            # Vérifier si MCP est activé
            if not yaml_config.get('mcp.enabled', True):
                # MCP désactivé, retourner un chemin vide
                return Path('mcp_config.json')  # Retourne quand même un chemin par défaut
            
            # Lire le chemin du fichier MCP
            mcp_config_file = yaml_config.get('mcp.config_file', 'mcp_config.json')
            
            # Résoudre le chemin relatif par rapport à la racine du projet
            project_root = Path(__file__).parent.parent.parent
            return project_root / mcp_config_file
            
        except Exception:
            # Si config.yml n'est pas accessible, chercher à la racine
            project_root = Path(__file__).parent.parent.parent
            return project_root / 'mcp_config.json'
    
    def _check_if_enabled(self) -> bool:
        """Vérifie si MCP est activé dans config.yml"""
        try:
            from hello_pulse.config import Config
            yaml_config = Config()
            return yaml_config.get('mcp.enabled', True)
        except Exception:
            # Par défaut, considérer comme activé
            return True
    
    def _load_config(self) -> Dict:
        """Charge le fichier de configuration JSON"""
        if not self.config_path.exists():
            return {"mcpServers": {}}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de parsing JSON dans {self.config_path}: {e}")
    
    def _replace_env_vars(self, value: str) -> str:
        """
        Remplace les variables d'environnement dans une chaîne.
        
        Supporte les formats:
        - ${VAR_NAME}
        - $VAR_NAME
        
        Exemple: "${TAVILY_API_KEY}" -> valeur de TAVILY_API_KEY
        """
        if not isinstance(value, str):
            return value
        
        # Pattern pour ${VAR_NAME} et $VAR_NAME
        pattern = r'\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?'
        
        def replacer(match):
            var_name = match.group(1)
            return os.getenv(var_name, '')
        
        return re.sub(pattern, replacer, value)
    
    def _prepare_env(self, env_config: Dict[str, str]) -> Dict[str, str]:
        """
        Prépare les variables d'environnement pour un serveur.
        
        Remplace les références aux variables d'environnement.
        """
        return {
            key: self._replace_env_vars(value)
            for key, value in env_config.items()
        }
    
    def _resolve_command(self, command: str) -> str:
        """
        Résout la commande en chemin absolu si nécessaire.
        
        Gère les cas spéciaux:
        - "python" -> sys.executable (interpréteur actuel)
        - "${PYTHON}" -> sys.executable
        """
        if command in ("python", "python3", "${PYTHON}"):
            return sys.executable
        
        return command
    
    def is_enabled(self) -> bool:
        """
        Vérifie si MCP est activé globalement.
        
        Returns:
            True si MCP est activé dans config.yml
        """
        return self._mcp_enabled
    
    def load_server(self, name: str) -> Optional[MCPServerStdio]:
        """
        Charge un serveur MCP spécifique par son nom.
        
        Args:
            name: Nom du serveur dans mcp_config.json
            
        Returns:
            MCPServerStdio configuré, ou None si non trouvé/désactivé
        """
        # Vérifier si MCP est activé globalement
        if not self._mcp_enabled:
            return None
        
        servers_config = self._config.get('mcpServers', {})
        server_config = servers_config.get(name)
        
        if not server_config:
            return None
        
        # Vérifier si le serveur est désactivé
        if server_config.get('disabled', False):
            return None
        
        # Récupérer la configuration
        command = server_config.get('command')
        args = server_config.get('args', [])
        env_config = server_config.get('env', {})
        
        if not command:
            raise ValueError(f"Server '{name}' has no command specified")
        
        # Résoudre la commande
        command = self._resolve_command(command)
        
        # Préparer l'environnement
        env = self._prepare_env(env_config)
        
        # Créer le serveur
        server = MCPServerStdio(
            command=command,
            args=args,
            env=env
        )
        
        return server
    
    def load_all_servers(self) -> List[MCPServerStdio]:
        """
        Charge tous les serveurs MCP configurés (non désactivés).
        
        Returns:
            Liste des serveurs MCP configurés
        """
        # Si MCP est désactivé, retourner une liste vide
        if not self._mcp_enabled:
            return []
        
        servers = []
        servers_config = self._config.get('mcpServers', {})
        
        for name in servers_config.keys():
            try:
                server = self.load_server(name)
                if server:
                    servers.append(server)
            except Exception as e:
                print(f"⚠️  Impossible de charger le serveur '{name}': {e}")
        
        return servers
    
    def get_server_names(self, include_disabled: bool = False) -> List[str]:
        """
        Liste les noms des serveurs configurés.
        
        Args:
            include_disabled: Inclure les serveurs désactivés
            
        Returns:
            Liste des noms de serveurs
        """
        servers_config = self._config.get('mcpServers', {})
        
        if include_disabled:
            return list(servers_config.keys())
        
        return [
            name for name, config in servers_config.items()
            if not config.get('disabled', False)
        ]
    
    def is_server_enabled(self, name: str) -> bool:
        """
        Vérifie si un serveur est activé.
        
        Args:
            name: Nom du serveur
            
        Returns:
            True si le serveur est activé (ou n'a pas de flag disabled)
        """
        servers_config = self._config.get('mcpServers', {})
        server_config = servers_config.get(name, {})
        return not server_config.get('disabled', False)
    
    def get_config_path(self) -> Path:
        """
        Retourne le chemin du fichier de configuration.
        
        Returns:
            Path du fichier mcp_config.json
        """
        return self.config_path


# ============================================================================
# Fonctions de commodité pour usage simple
# ============================================================================

def load_mcp_servers(config_path: Optional[str] = None) -> List[MCPServerStdio]:
    """
    Charge tous les serveurs MCP depuis mcp_config.json.
    
    Le chemin du fichier est automatiquement lu depuis config.yml si disponible.
    
    Args:
        config_path: Chemin optionnel vers le fichier de config (sinon auto-détecté)
        
    Returns:
        Liste des serveurs MCP configurés
    """
    loader = MCPConfigLoader(config_path)
    return loader.load_all_servers()



def load_canva_servers(config_path: Optional[str] = None) -> List[MCPServerStdio]:
    """
    Charge les serveurs MCP pour le Canvas (Agent Facilitateur).
    
    Pour l'instant : Tavily uniquement
    Futur : Peut inclure d'autres MCP spécifiques Canvas
    
    Args:
        config_path: Chemin optionnel vers le fichier de config (sinon auto-détecté)
        
    Returns:
        Liste des serveurs MCP pour Canvas
        
    Example:
        ```python
        from hello_pulse.mcp import load_canva_servers
        from pydantic_ai import Agent
        
        # Pour l'agent facilitateur Canvas
        servers = load_canva_servers()
        agent = Agent('gemini-2.0-flash', toolsets=servers)
        ```
    """
    loader = MCPConfigLoader(config_path)
    
    # Pour l'instant : Tavily uniquement
    # Futur : ajouter d'autres serveurs spécifiques Canvas
    servers = []
    tavily = loader.load_server('tavily')
    if tavily:
        servers.append(tavily)
    
    return servers
