"""
Module MCP pour Hello Pulse

Gère les connexions aux serveurs MCP (Model Context Protocol)
et expose les tools aux agents Pydantic AI.

Les serveurs MCP sont configurés dans mcp_config.json (format standard MCP).
Compatible avec Claude Desktop, Cline, et autres clients MCP.

La configuration peut être centralisée via config.yml qui pointe vers mcp_config.json.
"""

# Client manager (pour usage avancé multi-serveurs)
from hello_pulse.mcp.mcp_client import MCPManager

# Chargeur depuis JSON (MÉTHODE PRINCIPALE - dynamique)
from hello_pulse.mcp.mcp_config_loader import (
    MCPConfigLoader,
    load_mcp_servers,
    load_canva_servers
)

__all__ = [
    # Client manager
    'MCPManager',
    
    # Chargement dynamique depuis JSON (RECOMMANDÉ)
    'MCPConfigLoader',
    'load_mcp_servers',      # Pour Studio AI (tous les serveurs)
    'load_canva_servers',    # Pour Canvas/Facilitateur (subset)
]
