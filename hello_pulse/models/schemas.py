"""
Schémas Pydantic pour les réponses structurées de l'agent facilitateur
"""
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List


class PostureType(str, Enum):
    """Types de postures dynamiques de l'agent"""
    GUIDE = "guide"
    PROVOCATEUR = "provocateur"
    MEDIATEUR = "mediateur"
    TIMEKEEPER = "timekeeper"


class MessageType(str, Enum):
    """Types de messages de l'agent"""
    PUBLIC = "public"
    PRIVATE = "private"
    SYSTEM = "system"


class InterventionType(str, Enum):
    """Types d'interventions proactives"""
    SOLICITATION = "solicitation"          # Sollicitation participant silencieux
    FEEDBACK = "feedback"                  # Feedback participant dominant
    TRANSITION = "transition"              # Suggestion transition phase
    PAUSE = "pause"                        # Suggestion pause
    CHECK_IN = "check_in"                 # Check-in général


class AgentResponse(BaseModel):
    """Réponse structurée de l'agent facilitateur"""
    message: str = Field(description="Le message à afficher")
    message_type: MessageType = Field(description="Type de message (public/private/system)")
    target_user_id: Optional[str] = Field(
        default=None, 
        description="ID de l'utilisateur cible (pour messages privés)"
    )
    current_posture: PostureType = Field(description="Posture actuelle de l'agent")
    intervention_type: Optional[InterventionType] = Field(
        default=None,
        description="Type d'intervention (si proactive)"
    )


class MonitoringMetrics(BaseModel):
    """Métriques de monitoring pour décisions proactives"""
    participation_rate: dict[str, float]  # user_id -> pourcentage participation
    silence_duration: dict[str, int]      # user_id -> secondes de silence
    energy_level: float                   # Niveau d'énergie du groupe (0-100)
    phase_duration: int                   # Durée de la phase actuelle (secondes)
    total_ideas: int                      # Nombre total d'idées
    alert_score: int                      # Score d'alerte (0-100)


class SessionContext(BaseModel):
    """Contexte de la session pour l'agent"""
    session_id: str
    phase: str  # "divergence", "convergence", "priorisation"
    participants: List[dict]  # Liste des participants
    current_ideas: List[str]  # Idées actuelles
    metrics: MonitoringMetrics