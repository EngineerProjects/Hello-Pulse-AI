"""
Factories pour créer des sessions de chat avec différents agents
"""
import httpx
from hello_pulse.chat.sessions.facilitator_session import FacilitatorChatSession
from hello_pulse.chat.sessions.assistant_session import AssistantChatSession
from hello_pulse.agents.facilitator.agent import facilitator_agent
from hello_pulse.agents.facilitator.dependencies import FacilitatorDeps
from hello_pulse.agents.assistant.agent import assistant_agent
from hello_pulse.agents.assistant.dependencies import AssistantDeps
from hello_pulse.data_providers.base_provider import BaseDataProvider
from hello_pulse.data_providers.mock_provider import MockDataProvider
from hello_pulse.models.schemas import PostureType
from hello_pulse.prompts.facilitator.prompts import FacilitatorPrompts
from hello_pulse.prompts.assistant import AssistantPrompts
from hello_pulse.config import Config


async def create_facilitator_deps(
    data_provider: BaseDataProvider,
    http_client: httpx.AsyncClient,
    current_posture: PostureType = PostureType.GUIDE
) -> FacilitatorDeps:
    """
    Factory pour créer les dépendances du facilitator agent.
    
    Args:
        data_provider: Fournisseur de données
        http_client: Client HTTP async
        current_posture: Posture initiale de l'agent
        
    Returns:
        FacilitatorDeps configurées
    """
    prompts = FacilitatorPrompts()
    
    return FacilitatorDeps(
        data_provider=data_provider,
        http_client=http_client,
        prompts=prompts,
        current_posture=current_posture
    )


def create_facilitator_session(
    session_id: str = "facilitator-session",
    data_provider: BaseDataProvider = None,
    initial_posture: PostureType = PostureType.GUIDE
) -> FacilitatorChatSession:
    """
    Crée une session de chat avec l'agent facilitateur.
    
    Args:
        session_id: ID de la session
        data_provider: Fournisseur de données (Mock par défaut)
        initial_posture: Posture initiale de l'agent
        
    Returns:
        FacilitatorChatSession configurée pour le facilitator
    """
    # Utiliser MockDataProvider par défaut avec config
    if data_provider is None:
        config = Config()
        mock_config = config.get('data_providers.mock', {})
        
        data_provider = MockDataProvider(
            session_id=session_id,
            random_mode=mock_config.get('random_mode', True),
            config=mock_config
        )
    
    # Factory pour les dépendances avec la posture initiale
    async def deps_factory(data_provider, http_client):
        return await create_facilitator_deps(
            data_provider=data_provider,
            http_client=http_client,
            current_posture=initial_posture
        )
    
    return FacilitatorChatSession(
        agent=facilitator_agent,
        agent_deps_factory=deps_factory,
        data_provider=data_provider,
        session_id=session_id
    )



# ============================================================================
# ASSISTANT AGENT FACTORIES
# ============================================================================

async def create_assistant_deps(
    prompts: AssistantPrompts,
    http_client: httpx.AsyncClient,
    session_id: str,
    user_id: str = "user",
    user_role: str = "participant",
    session_phase: str = "divergence"
) -> AssistantDeps:
    """
    Factory pour créer les dépendances de l'assistant agent.
    
    Args:
        prompts: Gestionnaire de prompts
        http_client: Client HTTP async
        session_id: ID de la session
        user_id: ID de l'utilisateur
        user_role: Rôle de l'utilisateur
        session_phase: Phase actuelle de la session
        
    Returns:
        AssistantDeps configurées
    """
    return AssistantDeps(
        prompts=prompts,
        http_client=http_client,
        session_id=session_id,
        user_id=user_id,
        user_role=user_role,
        session_phase=session_phase
    )


def create_assistant_session(
    session_id: str = "assistant-session",
    user_id: str = "user",
    user_role: str = "participant",
    session_phase: str = "divergence"
) -> AssistantChatSession:
    """
    Crée une session de chat avec l'agent assistant.
    
    Args:
        session_id: ID de la session
        user_id: ID de l'utilisateur
        user_role: Rôle de l'utilisateur
        session_phase: Phase actuelle de la session
        
    Returns:
        AssistantChatSession configurée pour l'assistant
    """
    prompts = AssistantPrompts()
    
    # L'assistant n'a pas besoin de data provider
    # On crée un mock vide juste pour la compatibilité
    data_provider = MockDataProvider(session_id=session_id, random_mode=False)
    
    # Créer la session
    session = AssistantChatSession(
        agent=assistant_agent,
        agent_deps_factory=lambda dp, hc: None,  # Placeholder temporaire
        data_provider=data_provider,
        session_id=session_id,
        user_id=user_id,
        user_role=user_role
    )
    
    # Factory qui capture la session et utilise ses valeurs ACTUELLES
    async def deps_factory(data_provider, http_client):
        return await create_assistant_deps(
            prompts=prompts,
            http_client=http_client,
            session_id=session.session_id,
            user_id=session._user_id,
            user_role=session._user_role,
            session_phase=session._session_phase  # Valeur actuelle au moment de l'appel
        )
    
    # Remplacer par la vraie factory
    session.agent_deps_factory = deps_factory
    
    return session
