"""
Tests pour l'agent assistant

Ce script permet de tester l'agent assistant de manière interactive.
Il utilise le MCP Tavily pour les recherches web.
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

# Charger les variables d'environnement
project_root = Path(__file__).parent.parent
load_dotenv(project_root / '.env')

sys.path.append(str(project_root))
sys.path.append(str(project_root))

import asyncio
import httpx
from hello_pulse.agents.assistant import assistant_agent, AssistantDeps
from hello_pulse.prompts.assistant import AssistantPrompts


async def test_basic_qa():
    """Test de Q&A simple sans recherche web"""
    print("\n" + "="*60)
    print("TEST 1 : Q&A Simple (sans recherche web)")
    print("="*60)
    
    prompts = AssistantPrompts()
    
    async with httpx.AsyncClient() as client:
        deps = AssistantDeps(
            prompts=prompts,
            http_client=client,
            session_id="test-001",
            user_id="user-123",
            user_role="participant",
            session_phase="divergence"
        )
        
        question = "C'est quoi la méthode SCAMPER exactement ?"
        print(f"\n🙋 Question : {question}")
        print("\n⏳ L'agent réfléchit...\n")
        
        try:
            async with assistant_agent:
                result = await assistant_agent.run(question, deps=deps)
                print(f"🤖 Réponse :\n{result.output}")
                print(f"\n📊 Usage : {result.usage()}")
        except Exception as e:
            print(f"❌ Erreur : {e}")


async def test_web_search():
    """Test avec recherche web (MCP Tavily)"""
    print("\n" + "="*60)
    print("TEST 2 : Recherche Web (avec MCP Tavily)")
    print("="*60)
    
    prompts = AssistantPrompts()
    
    async with httpx.AsyncClient() as client:
        deps = AssistantDeps(
            prompts=prompts,
            http_client=client,
            session_id="test-002",
            user_id="user-456",
            user_role="participant",
            session_phase="divergence"
        )
        
        question = "Quelles sont les dernières tendances en IA générative en 2025 ?"
        print(f"\n🙋 Question : {question}")
        print("\n⏳ L'agent va rechercher sur le web...\n")
        
        try:
            async with assistant_agent:
                result = await assistant_agent.run(question, deps=deps)
                print(f"🤖 Réponse :\n{result.output}")
                print(f"\n📊 Usage : {result.usage()}")
        except Exception as e:
            print(f"❌ Erreur : {e}")


async def test_contextual_response():
    """Test avec contexte de session différent"""
    print("\n" + "="*60)
    print("TEST 3 : Réponse Contextuelle (phase convergence)")
    print("="*60)
    
    prompts = AssistantPrompts()
    
    async with httpx.AsyncClient() as client:
        deps = AssistantDeps(
            prompts=prompts,
            http_client=client,
            session_id="test-003",
            user_id="user-789",
            user_role="facilitateur",
            session_phase="convergence"
        )
        
        question = "Comment puis-je aider mon équipe à prioriser nos 20 idées ?"
        print(f"\n🙋 Question : {question}")
        print("📍 Contexte : Phase de convergence, rôle facilitateur")
        print("\n⏳ L'agent réfléchit...\n")
        
        try:
            async with assistant_agent:
                result = await assistant_agent.run(question, deps=deps)
                print(f"🤖 Réponse :\n{result.output}")
                print(f"\n📊 Usage : {result.usage()}")
        except Exception as e:
            print(f"❌ Erreur : {e}")


async def main():
    """Lance tous les tests"""
    print("\n" + "🎯 "*20)
    print("TESTS DE L'AGENT ASSISTANT - HELLO PULSE")
    print("🎯 "*20)
    
    # Test 1 : Q&A simple
    await test_basic_qa()
    
    # Pause
    await asyncio.sleep(2)
    
    # Test 2 : Avec recherche web
    await test_web_search()
    
    # Pause
    await asyncio.sleep(2)
    
    # Test 3 : Contextuel
    await test_contextual_response()
    
    print("\n" + "✅ "*20)
    print("TESTS TERMINÉS")
    print("✅ "*20 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
