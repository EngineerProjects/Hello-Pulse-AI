#!/usr/bin/env python3
"""
Script de vérification rapide de l'intégrité du projet Hello Pulse
Vérifie que tous les imports fonctionnent et que la configuration est valide
"""
import sys
from pathlib import Path

# Ajouter le projet au path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_imports():
    """Vérifie que tous les modules s'importent correctement"""
    print("🔍 Vérification des imports...")
    
    try:
        from hello_pulse.config import Config
        print("  ✅ hello_pulse.config")
        
        from hello_pulse.models.schemas import (
            PostureType, AgentResponse, SessionContext, MonitoringMetrics
        )
        print("  ✅ hello_pulse.models.schemas")
        
        from hello_pulse.data_providers.base_provider import BaseDataProvider
        from hello_pulse.data_providers.mock_provider import MockDataProvider
        print("  ✅ hello_pulse.data_providers")
        
        from hello_pulse.prompts.facilitator.prompts import FacilitatorPrompts
        print("  ✅ hello_pulse.prompts.facilitator")
        
        from hello_pulse.mcp import load_mcp_servers, load_canva_servers, MCPManager
        print("  ✅ hello_pulse.mcp")
        
        # Note: On ne peut pas importer chat.facilitator_session sans API key
        # car il importe l'agent qui s'initialise au module level
        from hello_pulse.chat.chat_session import ChatSession
        print("  ✅ hello_pulse.chat (base)")
        
        print("  ℹ️  Agent facilitateur non importé (nécessite GOOGLE_API_KEY)")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Erreur d'import : {e}")
        return False


def check_config():
    """Vérifie que la configuration se charge correctement"""
    print("\n🔍 Vérification de la configuration...")
    
    try:
        from hello_pulse.config import Config
        config = Config()
        
        # Vérifier quelques clés importantes
        model_name = config.get('agents.facilitator.model.name')
        if model_name:
            print(f"  ✅ Model configuré : {model_name}")
        else:
            print("  ⚠️  Model name non trouvé dans config")
            
        temp = config.get('agents.facilitator.model.temperature')
        if temp is not None:
            print(f"  ✅ Temperature : {temp}")
        else:
            print("  ⚠️  Temperature non trouvée dans config")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur de configuration : {e}")
        return False


def check_prompts():
    """Vérifie que les fichiers de prompts existent"""
    print("\n🔍 Vérification des fichiers prompts...")
    
    try:
        from hello_pulse.prompts.facilitator.prompts import FacilitatorPrompts
        prompts = FacilitatorPrompts()
        
        # Vérifier base_instructions
        base = prompts.get_base_instructions()
        if base and len(base) > 0:
            print(f"  ✅ base_instructions.txt ({len(base)} caractères)")
        else:
            print("  ❌ base_instructions.txt vide ou manquant")
            
        # Vérifier postures
        postures = ['guide', 'provocateur', 'mediateur', 'timekeeper']
        for posture in postures:
            try:
                prompt = prompts.get_posture_prompt(posture)
                if prompt and len(prompt) > 0:
                    print(f"  ✅ postures/{posture}.txt ({len(prompt)} caractères)")
                else:
                    print(f"  ⚠️  postures/{posture}.txt vide")
            except FileNotFoundError:
                print(f"  ❌ postures/{posture}.txt manquant")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur : {e}")
        return False


def check_mock_provider():
    """Vérifie que MockDataProvider fonctionne"""
    print("\n🔍 Vérification de MockDataProvider...")
    
    try:
        import asyncio
        from hello_pulse.data_providers.mock_provider import MockDataProvider
        
        async def test_provider():
            provider = MockDataProvider(session_id="test")
            ctx = await provider.get_session_context()
            
            print(f"  ✅ Session context créé")
            print(f"  ✅ Participants : {len(ctx.participants)}")
            print(f"  ✅ Phase : {ctx.phase}")
            print(f"  ✅ Idées : {ctx.metrics.total_ideas}")
            
            return True
        
        return asyncio.run(test_provider())
        
    except Exception as e:
        print(f"  ❌ Erreur : {e}")
        return False


def main():
    """Lance toutes les vérifications"""
    print("="*60)
    print("🚀 VÉRIFICATION HELLO PULSE AI")
    print("="*60 + "\n")
    
    results = []
    
    results.append(("Imports", check_imports()))
    results.append(("Configuration", check_config()))
    results.append(("Prompts", check_prompts()))
    results.append(("MockDataProvider", check_mock_provider()))
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n🎉 Toutes les vérifications ont réussi !")
        return 0
    else:
        print("\n⚠️  Certaines vérifications ont échoué")
        return 1


if __name__ == "__main__":
    sys.exit(main())
