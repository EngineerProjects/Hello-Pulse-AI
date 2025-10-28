"""
Handlers CLI pour tous les agents
"""
from .facilitator_handler import FacilitatorHandler
from .assistant_handler import AssistantHandler
from .general_handler import GeneralHandler
__all__ = [
    'FacilitatorHandler',
    'AssistantHandler',
    'GeneralHandler'
]