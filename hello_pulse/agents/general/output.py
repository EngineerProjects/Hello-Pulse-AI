"""
Modèle de sortie structuré pour l'Agent General

Définit la structure des réponses de l'agent avec :
- Raisonnement explicite
- Actions effectuées
- Résultat final
- Indicateur d'objectif atteint
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class GeneralOutput(BaseModel):
    """
    Sortie structurée de l'Agent General.
    
    Cette structure permet de :
    - Suivre le raisonnement de l'agent
    - Connaître les actions effectuées
    - Évaluer si l'objectif est atteint
    - Planifier les prochaines étapes si nécessaire
    """
    
    reasoning: str = Field(
        description="Raisonnement et analyse de l'agent pour accomplir la tâche"
    )
    
    actions_taken: List[str] = Field(
        description="Liste des actions et tools utilisés durant l'exécution",
        default_factory=list
    )
    
    result: str = Field(
        description="Résultat final de la tâche, présenté de manière claire et structurée"
    )
    
    goal_achieved: bool = Field(
        description="Indicateur si l'objectif principal de la tâche est atteint (true) ou non (false)"
    )
    
    confidence: float = Field(
        description="Niveau de confiance dans le résultat (0.0 à 1.0)",
        ge=0.0,
        le=1.0,
        default=0.8
    )
    
    next_steps: Optional[List[str]] = Field(
        description="Prochaines étapes recommandées si l'objectif n'est pas complètement atteint",
        default=None
    )
    
    artifacts_created: List[str] = Field(
        description="Liste des fichiers, rapports ou artefacts créés durant l'exécution",
        default_factory=list
    )