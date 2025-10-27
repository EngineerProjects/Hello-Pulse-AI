"""
Dépendances spécifiques à l'agent assistant
"""
from dataclasses import dataclass, field
from typing import Optional
import httpx

from hello_pulse.prompts.assistant.prompts import AssistantPrompts


@dataclass
class AssistantDeps:
    """
    Dépendances injectées dans l'agent assistant.
    
    L'assistant est plus simple que le facilitateur :
    - Pas de monitoring en temps réel
    - Pas de postures dynamiques
    - Mode réactif uniquement
    
    Attributes:
        prompts: Gestionnaire de prompts pour l'assistant
        http_client: Client HTTP pour requêtes async
        session_id: ID de la session Canvas actuelle
        user_id: ID de l'utilisateur qui sollicite l'assistant
        user_role: Rôle de l'utilisateur (participant, facilitateur, etc.)
        session_phase: Phase actuelle de la session (divergence, convergence, etc.)
        context: Contexte additionnel optionnel (métadonnées, préférences, etc.)
    """
    prompts: AssistantPrompts
    http_client: httpx.AsyncClient
    session_id: str
    user_id: str = "unknown"
    user_role: str = "participant"
    session_phase: str = "divergence"
    context: Optional[dict] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validation post-initialisation"""
        if not self.session_id:
            raise ValueError("session_id cannot be empty")
        
        # S'assurer que context est un dict
        if self.context is None:
            self.context = {}
