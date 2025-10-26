"""
Agent Facilitateur pour Hello Pulse - Sessions de brainstorming en temps réel
"""
from pydantic_ai import Agent, RunContext
from hello_pulse.config import Config
import os

from hello_pulse.models.schemas import AgentResponse, PostureType
from hello_pulse.agents.facilitator.dependencies import FacilitatorDeps


# Charger la configuration depuis config.yml
config = Config()
facilitator_config = config.get('agents.facilitator', {})
model_config = facilitator_config.get('model', {})

# Créer l'agent avec le nom du modèle (pas l'instance)
# Pydantic AI créera automatiquement un nouveau client pour chaque contexte
facilitator_agent = Agent(
    model=model_config.get('name', 'gemini-2.0-flash'),
    deps_type=FacilitatorDeps,
    output_type=AgentResponse,
    name="facilitator_agent",
    retries=2,
)


@facilitator_agent.system_prompt
def base_instructions(ctx: RunContext[FacilitatorDeps]) -> str:
    """Instructions de base statiques"""
    return ctx.deps.prompts.get_base_instructions()


@facilitator_agent.system_prompt
def dynamic_posture_instructions(ctx: RunContext[FacilitatorDeps]) -> str:
    """Instructions dynamiques selon la posture actuelle"""
    posture = ctx.deps.current_posture.value
    return f"""
Posture actuelle : {posture.upper()}

{ctx.deps.prompts.get_posture_prompt(posture)}
"""


@facilitator_agent.system_prompt
async def session_context_prompt(ctx: RunContext[FacilitatorDeps]) -> str:
    """Contexte de la session actuelle"""
    # Récupérer le contexte depuis le data provider
    session_context = await ctx.deps.data_provider.get_session_context()
    metrics = session_context.metrics
    
    return f"""
CONTEXTE DE LA SESSION :
- Session ID : {session_context.session_id}
- Phase actuelle : {session_context.phase}
- Nombre de participants : {len(session_context.participants)}
- Idées générées : {metrics.total_ideas}
- Durée de la phase : {metrics.phase_duration}s
- Niveau d'énergie du groupe : {metrics.energy_level}%

PARTICIPANTS :
{format_participants(session_context.participants, metrics)}
"""


def format_participants(participants: list, metrics) -> str:
    """Formate les infos des participants pour le prompt"""
    lines = []
    for p in participants:
        user_id = p['id']
        name = p['name']
        participation = metrics.participation_rate.get(user_id, 0)
        silence = metrics.silence_duration.get(user_id, 0)
        
        lines.append(
            f"- {name} (ID: {user_id}): "
            f"Participation {participation:.1f}%, "
            f"Silencieux depuis {silence}s"
        )
    
    return '\n'.join(lines)


@facilitator_agent.tool
async def get_session_metrics(ctx: RunContext[FacilitatorDeps]) -> dict:
    """Récupère les métriques de monitoring de la session"""
    metrics = await ctx.deps.data_provider.get_current_metrics()
    return {
        "alert_score": metrics.alert_score,
        "energy_level": metrics.energy_level,
        "phase_duration": metrics.phase_duration,
        "total_ideas": metrics.total_ideas,
        "participation_summary": metrics.participation_rate
    }


@facilitator_agent.tool
async def get_participant_info(
    ctx: RunContext[FacilitatorDeps], 
    user_id: str
) -> dict:
    """Récupère les informations détaillées d'un participant"""
    session_context = await ctx.deps.data_provider.get_session_context()
    participants = session_context.participants
    participant = next((p for p in participants if p['id'] == user_id), None)
    
    if not participant:
        return {"error": f"Participant {user_id} not found"}
    
    metrics = session_context.metrics
    return {
        "name": participant['name'],
        "role": participant.get('role', 'participant'),
        "expertise": participant.get('expertise', []),
        "participation_rate": metrics.participation_rate.get(user_id, 0),
        "silence_duration": metrics.silence_duration.get(user_id, 0)
    }


# Fonction helper pour changer de posture
async def change_posture(
    new_posture: PostureType,
    deps: FacilitatorDeps
) -> None:
    """Change la posture de l'agent"""
    deps.current_posture = new_posture
