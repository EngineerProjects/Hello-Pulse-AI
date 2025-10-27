"""
Utilitaires pour charger les serveurs MCP depuis config.yml
"""
from typing import List
from pydantic_ai.mcp import MCPServerStdio
from hello_pulse.mcp.mcp_config_loader import MCPConfigLoader


def load_mcp_servers_for_agent(
    tools_mcp_list: List[str],
    agent_name: str
) -> List[MCPServerStdio]:
    """
    Charge les serveurs MCP pour un agent spécifique.
    
    Args:
        tools_mcp_list: Liste des noms de tools MCP à charger
        agent_name: Nom de l'agent (pour les logs)
        
    Returns:
        Liste des serveurs MCP chargés
    """
    mcp_loader = MCPConfigLoader()
    
    if not mcp_loader.is_enabled():
        print(f"⚠️  MCP désactivé pour {agent_name}")
        return []
    
    mcp_servers = []
    failed_tools = []
    
    for tool_name in tools_mcp_list:
        try:
            server = mcp_loader.load_server(tool_name)
            if server:
                mcp_servers.append(server)
                print(f"   ✅ {tool_name} chargé")
            else:
                failed_tools.append(tool_name)
        except Exception as e:
            failed_tools.append(tool_name)
            print(f"   ❌ {tool_name}: {e}")
    
    if failed_tools:
        print(f"   ⚠️  Tools non chargés: {', '.join(failed_tools)}")
    
    return mcp_servers