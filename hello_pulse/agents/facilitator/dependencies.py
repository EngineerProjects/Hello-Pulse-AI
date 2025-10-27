from dataclasses import dataclass
from typing import Optional
import httpx

from hello_pulse.models.schemas import PostureType
from hello_pulse.prompts.facilitator.prompts import FacilitatorPrompts
from hello_pulse.data_providers.base_provider import BaseDataProvider


@dataclass
class FacilitatorDeps:
    """
    Dépendances injectées dans l'agent facilitateur.
    
    Ces dépendances sont spécifiques au facilitator et utilisent
    le pattern de data provider pour récupérer les données.
    
    Attributes:
        data_provider: Provider pour accéder aux données de session
        http_client: Client HTTP asynchrone pour requêtes externes
        prompts: Gestionnaire de prompts système et postures
        current_posture: Posture active de l'agent (par défaut: GUIDE)
        db_connection: Connexion base de données (future utilisation)
    """
    data_provider: BaseDataProvider
    http_client: httpx.AsyncClient
    prompts: FacilitatorPrompts
    current_posture: PostureType = PostureType.GUIDE
    db_connection: Optional[object] = None  # Pour future utilisation
    
    def __post_init__(self) -> None:
        """Validation post-initialisation"""
        if not isinstance(self.current_posture, PostureType):
            raise TypeError(
                f"current_posture must be PostureType, got {type(self.current_posture)}"
            )