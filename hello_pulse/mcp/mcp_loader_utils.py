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
    
    CORRECTION : Supporte le mot-clé '*' dans la liste 
    pour charger TOUS les serveurs MCP définis dans mcp_config.json.
    
    Args:
        tools_mcp_list: Liste des noms de tools MCP à charger (ou ["*"])
        agent_name: Nom de l'agent (pour les logs)
        
    Returns:
        Liste des serveurs MCP chargés
    """
    mcp_loader = MCPConfigLoader()
    
    if not mcp_loader.is_enabled():
        print(f"⚠️  MCP désactivé pour {agent_name}")
        return []

    # --- DÉBUT DE LA LOGIQUE CORRIGÉE ---
    # Vérifier si la liste contient le mot-clé "*"
    if tools_mcp_list and tools_mcp_list[0] == "*":
        print(f"   ℹ️  Agent '{agent_name}' demande TOUS les serveurs MCP...")
        try:
            # Charger tous les serveurs définis dans mcp_config.json
            all_servers = mcp_loader.load_all_servers()
            
            # Afficher les serveurs chargés
            server_names = [s.command for s in all_servers] # Simple façon de les lister
            print(f"   ✅ {len(all_servers)} serveurs chargés pour '{agent_name}'.")
            
            # Lister les noms pour vérification
            all_server_names = mcp_loader.get_server_names()
            for s_name in all_server_names:
                 print(f"      - {s_name}")
                 
            return all_servers
        
        except Exception as e:
            print(f"   ❌ Erreur critique lors du chargement de TOUS les serveurs: {e}")
            return []
    # --- FIN DE LA LOGIQUE CORRIGÉE ---

    # Si "*" n'est pas utilisé, on garde l'ancienne logique
    # (pour l'agent Assistant, par exemple)
    print(f"   ℹ️  Agent '{agent_name}' demande des serveurs spécifiques...")
    mcp_servers = []
    failed_tools = []
    
    if not tools_mcp_list:
        print("   (Aucun tool MCP configuré)")
        return []
    
    for tool_name in tools_mcp_list:
        try:
            server = mcp_loader.load_server(tool_name)
            if server:
                mcp_servers.append(server)
                print(f"   ✅ {tool_name} chargé")
            else:
                # Gère le cas où le tool est listé mais pas dans mcp_config.json
                print(f"   ❌ {tool_name}: Non trouvé dans mcp_config.json ou désactivé.")
                failed_tools.append(tool_name)
        except Exception as e:
            failed_tools.append(tool_name)
            print(f"   ❌ {tool_name}: Erreur au chargement - {e}")
    
    if failed_tools:
        print(f"   ⚠️  Tools non chargés: {', '.join(failed_tools)}")
    
    return mcp_servers