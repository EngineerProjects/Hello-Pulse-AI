"""
Agent General pour Hello Pulse - Agent autonome multi-tools

L'agent general est un agent autonome capable de travailler sur des tâches
complexes nécessitant plusieurs étapes et l'utilisation de multiples tools.

Caractéristiques :
- Mode autonome avec boucles itératives
- ReAct complet avec reasoning explicite
- Support de 10+ tools MCP (extensible)
- Sortie structurée avec évaluation d'objectif
- Temperature 0.8 (plus créatif et explorateur)
"""
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
from hello_pulse.config import Config
from hello_pulse.agents.general.dependencies import GeneralDeps
from hello_pulse.agents.general.output import GeneralOutput
from hello_pulse.mcp.mcp_config_loader import MCPConfigLoader
from hello_pulse.mcp.mcp_loader_utils import load_mcp_servers_for_agent

# Charger la configuration depuis config.yml
config = Config()
general_config = config.get('agents.general', {})
model_config = general_config.get('model', {})

# Charger les serveurs MCP depuis config.yml
tools_mcp_list = general_config.get('tools_mcp', [])
mcp_servers = load_mcp_servers_for_agent(tools_mcp_list, "General")

# Créer l'agent general avec configuration
general_agent = Agent(
    model=model_config.get('name', 'gemini-2.0-flash'),
    deps_type=GeneralDeps,
    output_type=GeneralOutput,  # Sortie structurée avec goal_achieved
    name="general_agent",
    toolsets=mcp_servers,  # Tous les MCP servers disponibles
    retries=3,  # Plus de retries pour gérer la complexité
    model_settings=ModelSettings(
        temperature=model_config.get('temperature', 0.8),
        max_tokens=model_config.get('max_tokens', 8192),
    ),
    instrument=True,  # Instrumentation pour capturer les tool calls
)


@general_agent.instructions
def base_instructions(ctx: RunContext[GeneralDeps]) -> str:
    """
    Instructions de base statiques pour l'agent general.
    
    Ces instructions définissent le rôle, les capacités et le workflow
    de l'agent autonome. Chargées depuis instructions.txt.
    """
    return ctx.deps.prompts.get_base_instructions()


@general_agent.instructions
def task_context(ctx: RunContext[GeneralDeps]) -> str:
    """
    Contexte dynamique de la tâche en cours.
    
    Fournit à l'agent :
    - Informations sur la session
    - Description de la tâche si disponible
    - Progression actuelle (itération)
    - Limites et contraintes
    """
    task_info = f"""
=== CONTEXTE DE LA TÂCHE ===

Session ID : {ctx.deps.session_id}
Utilisateur : {ctx.deps.user_id}
Itération : {ctx.deps.current_iteration}/{ctx.deps.max_iterations}
"""
    
    if ctx.deps.task_description:
        task_info += f"\nDescription de la tâche :\n{ctx.deps.task_description}\n"
    
    task_info += """
RAPPEL IMPORTANT :
- Utilise TOUS les tools nécessaires pour accomplir la tâche
- Sois méthodique : analyse → planifie → exécute → vérifie
- À la fin, évalue honnêtement si l'objectif est atteint (goal_achieved)
- Si non atteint, propose des next_steps concrets
"""
    
    return task_info


# Note : Les tools MCP (Tavily, Filesystem, Puppeteer, etc.) sont automatiquement
# disponibles via le paramètre toolsets de l'agent.
# Pydantic AI gère le ReAct automatiquement avec ces tools.