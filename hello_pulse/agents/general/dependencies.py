"""
Dépendances pour l'Agent General

Contient toutes les données et services nécessaires à l'agent :
- Prompts système
- Client HTTP pour les appels externes
- Identifiants de session et utilisateur
"""
from dataclasses import dataclass
from typing import Optional
import httpx
from hello_pulse.prompts.general import GeneralPrompts


@dataclass
class GeneralDeps:
    """
    Dépendances injectées dans l'Agent General.
    
    Ces dépendances sont accessibles via RunContext dans :
    - Les instructions dynamiques
    - Les tools personnalisés (si ajoutés plus tard)
    """
    
    prompts: GeneralPrompts
    """Gestionnaire des prompts système"""
    
    http_client: httpx.AsyncClient
    """Client HTTP async pour appels externes (APIs, webhooks, etc.)"""
    
    session_id: str
    """Identifiant unique de la session en cours"""
    
    user_id: str = "user"
    """Identifiant de l'utilisateur qui a lancé la tâche"""
    
    task_description: Optional[str] = None
    """Description détaillée de la tâche à accomplir (optionnel)"""
    
    max_iterations: int = 20
    """Nombre maximum d'itérations autorisées pour la tâche"""
    
    current_iteration: int = 0
    """Itération actuelle (utilisé pour le suivi de progression)"""