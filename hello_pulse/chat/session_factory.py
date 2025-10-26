"""
Factories pour créer des sessions de chat avec différents agents
"""
import httpx
from hello_pulse.chat.facilitator_session import FacilitatorChatSession
from hello_pulse.agents.facilitator.agent import facilitator_agent
from hello_pulse.agents.facilitator.dependencies import FacilitatorDeps
from hello_pulse.data_providers.base_provider import BaseDataProvider
from hello_pulse.data_providers.mock_provider import MockDataProvider
from hello_pulse.models.schemas import PostureType
from hello_pulse.prompts.facilitator.prompts import FacilitatorPrompts
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
    initial_posture: PostureType = PostureType.GUIDE,
    save_history: bool = True
) -> FacilitatorChatSession:
    """
    Crée une session de chat avec l'agent facilitateur.
    
    Args:
        session_id: ID de la session
        data_provider: Fournisseur de données (Mock par défaut)
        initial_posture: Posture initiale de l'agent
        save_history: Sauvegarder l'historique automatiquement
        
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
        session_id=session_id,
        save_history=save_history
    )
