"""
Dépendances spécifiques à l'agent facilitateur
"""
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
    """
    data_provider: BaseDataProvider
    http_client: httpx.AsyncClient
    prompts: FacilitatorPrompts
    current_posture: PostureType = PostureType.GUIDE
    db_connection: Optional[object] = None  # Pour future utilisation
