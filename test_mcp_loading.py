"""
Script de test pour vérifier le chargement des MCP servers
"""
from hello_pulse.mcp.mcp_config_loader import MCPConfigLoader
from hello_pulse.config import Config

from dotenv import load_dotenv

load_dotenv('.env')

def test_mcp_loading():
    print("=== Test de chargement des MCP servers ===\n")
    
    # Test 1: Config.yml
    print("1. Vérification config.yml...")
    config = Config()
    assistant_config = config.get('agents.assistant', {})
    tools_mcp = assistant_config.get('tools_mcp', [])
    print(f"   Tools MCP configurés pour assistant: {tools_mcp}")
    
    # Test 2: MCP Config Loader
    print("\n2. Chargement MCP Config Loader...")
    loader = MCPConfigLoader()
    print(f"   MCP activé: {loader.is_enabled()}")
    print(f"   Chemin config: {loader.get_config_path()}")
    print(f"   Fichier existe: {loader.get_config_path().exists()}")
    
    # Test 3: Serveurs disponibles
    print("\n3. Serveurs disponibles...")
    server_names = loader.get_server_names()
    print(f"   Serveurs: {server_names}")
    
    # Test 4: Chargement de Tavily
    print("\n4. Chargement du serveur Tavily...")
    try:
        tavily_server = loader.load_server('tavily')
        if tavily_server:
            print(f"   ✅ Tavily chargé: {tavily_server}")
        else:
            print(f"   ❌ Tavily non chargé (retourne None)")
    except Exception as e:
        print(f"   ❌ Erreur lors du chargement: {e}")
    
    # Test 5: Vérification agent assistant
    print("\n5. Vérification de l'agent assistant...")
    try:
        from hello_pulse.agents.assistant.agent import assistant_agent, mcp_servers
        print(f"   Agent créé: {assistant_agent}")
        print(f"   Nombre de MCP servers: {len(mcp_servers)}")
        print(f"   MCP servers: {mcp_servers}")
        
        # Vérifier les toolsets de l'agent
        if hasattr(assistant_agent, '_toolsets'):
            print(f"   Toolsets de l'agent: {assistant_agent._toolsets}")
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mcp_loading()
