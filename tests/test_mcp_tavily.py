"""
Test d'intégration MCP Tavily

Ce test vérifie que le serveur MCP Tavily fonctionne correctement
avec Pydantic AI.

IMPORTANT - CYCLE DE VIE MCP (CORRIGÉ):
- Chaque test doit créer son PROPRE agent ET serveur MCP
- Le contexte `async with agent:` démarre et arrête le serveur automatiquement
- Ne JAMAIS réutiliser le même agent dans plusieurs contextes
- Alternative: Utiliser `async with agent.run_mcp_servers():` pour un cycle de vie plus long
"""
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
project_root = Path(__file__).parent.parent
load_dotenv(project_root / '.env')

sys.path.append(str(project_root))

from pydantic_ai import Agent
from hello_pulse.mcp import load_canva_servers, load_mcp_servers, MCPManager


async def test_tavily_direct():
    """Test direct du serveur Tavily MCP"""
    print("\n" + "="*60)
    print("TEST 1: Serveur Tavily MCP Direct (via load_canva_servers)")
    print("="*60)
    
    # IMPORTANT: Créer un NOUVEAU serveur pour ce test
    servers = load_canva_servers()
    
    # Créer un agent avec les serveurs Canvas (Tavily pour l'instant)
    agent = Agent(
        'gemini-2.0-flash',
        toolsets=servers,
        system_prompt="Tu es un assistant qui aide à faire des recherches web."
    )
    
    # Utiliser l'agent dans un contexte async
    # Le serveur MCP est démarré ici et fermé à la sortie du contexte
    async with agent:
        result = await agent.run(
            "Recherche les dernières nouvelles sur l'agriculture durable en Afrique"
        )
        
        print(f"\n✅ Réponse de l'agent:")
        print(result.output)


async def test_mcp_manager():
    """Test avec le MCPManager"""
    print("\n" + "="*60)
    print("TEST 2: MCPManager")
    print("="*60)
    
    # IMPORTANT: Créer un NOUVEAU manager pour ce test
    # Chaque test doit avoir ses propres serveurs MCP frais
    mcp_manager = MCPManager()
    
    # Charger tous les serveurs depuis mcp_config.json
    servers = load_mcp_servers()
    for i, server in enumerate(servers):
        mcp_manager.add_server(f'server_{i}', server)
    
    print(f"📋 Serveurs enregistrés: {mcp_manager.list_servers()}")
    
    # IMPORTANT: Créer un NOUVEL agent avec les serveurs du manager
    agent = Agent(
        'gemini-2.0-flash',
        toolsets=mcp_manager.get_all_servers(),
        system_prompt="Tu es un assistant de recherche. Utilise la recherche web pour répondre."
    )
    
    # Le contexte async with agent gère le cycle de vie des serveurs
    async with agent:
        result = await agent.run(
            "Recherche sur internet les innovations récentes en aquaponie"
        )
        
        print(f"\n✅ Réponse de l'agent:")
        print(result.output)


async def test_facilitator_with_mcp():
    """Test simplifié: Agent générique avec MCP Tavily"""
    print("\n" + "="*60)
    print("TEST 3: Agent Canvas + Facilitateur (load_canva_servers)")
    print("="*60)
    
    # Test simplifié: on teste juste qu'un agent avec system prompt 
    # peut utiliser MCP Tavily via load_canva_servers
    servers = load_canva_servers()
    
    agent = Agent(
        model='gemini-2.0-flash',
        toolsets=servers,
        system_prompt="""Tu es un facilitateur de brainstorming.
        Tu aides à trouver des exemples et références pour inspirer les participants.
        Utilise la recherche web pour trouver des informations pertinentes."""
    )
    
    async with agent:
        result = await agent.run(
            "Trouve 2-3 exemples d'ateliers de design thinking réussis"
        )
        
        print(f"\n✅ Réponse de l'agent:")
        print(result.output)


async def test_interactive_mode():
    """Test du mode interactif avec run_mcp_servers()"""
    print("\n" + "="*60)
    print("TEST 4: Mode Interactif Canvas (run_mcp_servers)")
    print("="*60)
    
    # Pour une utilisation interactive, on peut utiliser run_mcp_servers()
    # qui garde le serveur actif plus longtemps
    servers = load_canva_servers()
    agent = Agent(
        'gemini-2.0-flash',
        toolsets=servers,
        system_prompt="Tu es un assistant de recherche."
    )
    
    # run_mcp_servers() permet de faire plusieurs requêtes dans le même contexte
    async with agent.run_mcp_servers():
        # Première requête
        result1 = await agent.run("Recherche les tendances IA 2025")
        print(f"\n✅ Requête 1: {result1.output}")
        
        # Deuxième requête - fonctionne car on est dans le même contexte
        result2 = await agent.run("Recherche les applications de l'IA en agriculture")
        print(f"\n✅ Requête 2: {result2.output}")


async def main():
    """Lance tous les tests"""
    try:
        # Test 1: Tavily direct
        print("\n🔄 Test 1/4: Tavily Direct...")
        await test_tavily_direct()
        
        # IMPORTANT: Petit délai entre les tests pour laisser les ressources se fermer proprement
        print("\n⏸️  Pause entre les tests...")
        await asyncio.sleep(2)
        
        # Test 2: MCPManager
        print("\n🔄 Test 2/4: MCPManager...")
        await test_mcp_manager()
        
        # Pause entre les tests
        print("\n⏸️  Pause entre les tests...")
        await asyncio.sleep(2)
        
        # Test 3: Facilitateur avec MCP
        print("\n🔄 Test 3/4: Facilitateur...")
        await test_facilitator_with_mcp()
        
        # Pause entre les tests
        print("\n⏸️  Pause entre les tests...")
        await asyncio.sleep(2)
        
        # Test 4: Mode interactif
        print("\n🔄 Test 4/4: Mode Interactif...")
        await test_interactive_mode()
        
        print("\n" + "="*60)
        print("✅ Tous les tests MCP ont réussi!")
        print("="*60)
        
    except Exception as e:
        # Gestion des erreurs avec messages plus clairs
        error_msg = str(e)
        
        print(f"\n❌ Erreur lors des tests: {error_msg}")
        
        # Messages d'aide selon le type d'erreur
        if "503" in error_msg or "overloaded" in error_msg.lower():
            print("\n💡 CONSEIL: Le modèle Google est temporairement surchargé.")
            print("   Réessayez dans quelques minutes ou utilisez un autre modèle.")
            print("   Exemple: Remplacez 'gemini-2.0-flash' par 'gemini-1.5-flash'")
        
        elif "closed" in error_msg.lower() or "httpx" in error_msg.lower():
            print("\n💡 CONSEIL: Le client HTTP s'est fermé.")
            print("   Vérifiez que chaque test crée son propre agent et serveur MCP.")
            print("   ✅ BON: Créer un nouvel agent pour chaque test")
            print("   ❌ MAUVAIS: Réutiliser le même agent dans plusieurs tests")
            print("\n   NOTE: Ce problème peut aussi se produire avec le modèle Google GenAI")
            print("   qui partage un client HTTP global. Essayez d'ajouter un délai entre tests.")
        
        elif "TAVILY_API_KEY" in error_msg:
            print("\n💡 CONSEIL: Clé API Tavily manquante ou invalide.")
            print("   Vérifiez le fichier .env")
        
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Vérifier que la clé API Tavily est présente
    if not os.getenv('TAVILY_API_KEY'):
        print("❌ ERREUR: TAVILY_API_KEY non trouvée dans .env")
        print("   Ajoutez TAVILY_API_KEY=votre_clé dans le fichier .env")
        exit(1)
    
    print("🚀 Lancement des tests MCP Tavily (VERSION CORRIGÉE)...")
    asyncio.run(main())
