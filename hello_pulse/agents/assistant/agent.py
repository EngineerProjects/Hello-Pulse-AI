"""
Agent Assistant pour Hello Pulse - Q&A réactif avec recherche web

L'agent assistant est un agent réactif qui aide les utilisateurs pendant
leurs sessions de brainstorming en répondant à leurs questions et en
effectuant des recherches web si nécessaire.

Caractéristiques :
- Mode réactif (répond uniquement quand sollicité)
- ReAct léger via tools MCP (Tavily pour recherche web)
- Réponses concises et factuelles
- Temperature 0.6 (plus factuel que créatif)
"""
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
from hello_pulse.config import Config
from hello_pulse.agents.assistant.dependencies import AssistantDeps
from hello_pulse.mcp.mcp_config_loader import MCPConfigLoader
from hello_pulse.mcp.mcp_loader_utils import load_mcp_servers_for_agent

# Charger la configuration depuis config.yml
config = Config()
assistant_config = config.get('agents.assistant', {})
model_config = assistant_config.get('model', {})

# Charger les serveurs MCP depuis config.yml
tools_mcp_list = assistant_config.get('tools_mcp', [])
mcp_servers = load_mcp_servers_for_agent(tools_mcp_list, "Assistant")

# Créer l'agent assistant avec configuration
assistant_agent = Agent(
    model=model_config.get('name', 'gemini-2.0-flash'),
    deps_type=AssistantDeps,
    output_type=str,
    name="assistant_agent",
    toolsets=mcp_servers,
    retries=2,
    model_settings=ModelSettings(
        temperature=model_config.get('temperature', 0.6),
        max_tokens=model_config.get('max_tokens', 2048),
    ),
    instrument=True,
)


@assistant_agent.instructions
def base_instructions(ctx: RunContext[AssistantDeps]) -> str:
    """
    Instructions de base statiques pour l'assistant.
    
    Ces instructions définissent le rôle, le style et les limites de l'assistant.
    Elles sont chargées depuis le fichier instructions.txt.
    """
    return ctx.deps.prompts.get_base_instructions()


@assistant_agent.instructions
def session_context(ctx: RunContext[AssistantDeps]) -> str:
    """
    Contexte dynamique de la session actuelle.
    
    Fournit à l'agent des informations sur :
    - La session en cours
    - L'utilisateur qui pose la question
    - La phase actuelle de la session
    
    Ces informations permettent à l'agent de contextualiser ses réponses.
    """
    return f"""
=== CONTEXTE DE LA SESSION ===

Session ID : {ctx.deps.session_id}
Phase actuelle : {ctx.deps.session_phase}
Utilisateur : {ctx.deps.user_id} ({ctx.deps.user_role})

Tu dois adapter tes réponses au contexte de la session.
Par exemple, si la phase est "divergence", encourage la génération d'idées.
Si c'est "convergence", aide à structurer et prioriser.
"""


# Note : Les tools MCP (comme Tavily) sont automatiquement disponibles
# via le paramètre toolsets de l'agent. Pas besoin de les définir ici.
# Pydantic AI gère le ReAct automatiquement quand des tools sont disponibles.
