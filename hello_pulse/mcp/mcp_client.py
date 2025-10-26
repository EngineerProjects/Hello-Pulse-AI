"""
Gestionnaire centralisé des serveurs MCP pour Hello Pulse

Permet de gérer plusieurs serveurs MCP et de les utiliser avec les agents Pydantic AI.
Utilise le loader dynamique pour charger les serveurs depuis mcp_config.json.
"""
from typing import Dict, List, Optional
from pydantic_ai.mcp import MCPServer


class MCPManager:
    """
    Gestionnaire centralisé pour tous les serveurs MCP.
    
    Simplifie l'initialisation et la gestion de plusieurs serveurs MCP,
    permet de les enregistrer et de les fournir aux agents.
    
    Example:
        ```python
        from hello_pulse.mcp import MCPManager, load_mcp_servers
        from pydantic_ai import Agent
        
        # Créer le manager
        mcp_manager = MCPManager()
        
        # Charger tous les serveurs depuis mcp_config.json
        servers = load_mcp_servers()
        for server in servers:
            mcp_manager.add_server('server_name', server)
        
        # Utiliser avec un agent
        agent = Agent('gemini-2.0-flash', toolsets=mcp_manager.get_all_servers())
        
        async with agent:
            result = await agent.run("Recherche sur l'agriculture durable")
        ```
    """
    
    def __init__(self):
        self._servers: Dict[str, MCPServer] = {}
    
    def add_server(self, name: str, server: MCPServer) -> 'MCPManager':
        """
        Ajoute un serveur MCP.
        
        Args:
            name: Nom du serveur
            server: Instance MCPServer
            
        Returns:
            self pour chaînage des méthodes
        """
        self._servers[name] = server
        return self
    
    def get_server(self, name: str) -> Optional[MCPServer]:
        """
        Récupère un serveur MCP par son nom.
        
        Args:
            name: Nom du serveur
            
        Returns:
            Le serveur MCP ou None si non trouvé
        """
        return self._servers.get(name)
    
    def get_all_servers(self) -> List[MCPServer]:
        """
        Récupère tous les serveurs MCP enregistrés.
        
        Returns:
            Liste de tous les serveurs MCP
        """
        return list(self._servers.values())
    
    def remove_server(self, name: str) -> bool:
        """
        Supprime un serveur MCP.
        
        Args:
            name: Nom du serveur à supprimer
            
        Returns:
            True si supprimé, False si non trouvé
        """
        if name in self._servers:
            del self._servers[name]
            return True
        return False
    
    def list_servers(self) -> List[str]:
        """
        Liste les noms de tous les serveurs enregistrés.
        
        Returns:
            Liste des noms de serveurs
        """
        return list(self._servers.keys())
    
    def has_server(self, name: str) -> bool:
        """
        Vérifie si un serveur est enregistré.
        
        Args:
            name: Nom du serveur
            
        Returns:
            True si le serveur existe
        """
        return name in self._servers
