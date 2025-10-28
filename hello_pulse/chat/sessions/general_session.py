"""
Session de chat spécialisée pour l'agent general.

Cette classe étend ChatSession avec des fonctionnalités spécifiques
au general comme la gestion des tâches autonomes et itérations.
"""
from typing import Optional
from hello_pulse.chat.chat_session import ChatSession


class GeneralChatSession(ChatSession):
    """
    Session de chat spécialisée pour l'agent general.
    
    L'agent general est autonome et peut :
    - Travailler sur des tâches complexes multi-étapes
    - Utiliser de nombreux tools MCP
    - Fonctionner en mode itératif
    - Évaluer si l'objectif est atteint
    """
    
    def __init__(self, *args, user_id: str = "user", **kwargs):
        super().__init__(*args, **kwargs)
        self._user_id = user_id
        self._current_task = None
        self._max_iterations = 20
        self._current_iteration = 0
    
    @property
    def user_id(self) -> str:
        """Retourne l'ID de l'utilisateur"""
        return self._user_id
    
    @property
    def current_task(self) -> Optional[str]:
        """Retourne la tâche en cours"""
        return self._current_task
    
    @property
    def max_iterations(self) -> int:
        """Retourne le nombre max d'itérations"""
        return self._max_iterations
    
    @property
    def current_iteration(self) -> int:
        """Retourne l'itération actuelle"""
        return self._current_iteration
    
    def set_task(self, task_description: str):
        """
        Définit la tâche principale à accomplir.
        
        Args:
            task_description: Description détaillée de la tâche
        """
        self._current_task = task_description
        self._current_iteration = 0
        print(f"📋 Nouvelle tâche définie : {task_description}")
    
    def increment_iteration(self):
        """Incrémente le compteur d'itérations"""
        self._current_iteration += 1
    
    def reset_iteration(self):
        """Remet le compteur d'itérations à zéro"""
        self._current_iteration = 0
    
    def get_context_info(self) -> dict:
        """
        Retourne les informations de contexte pour l'affichage.
        
        Returns:
            Dictionnaire avec le contexte actuel
        """
        return {
            'session_id': self.session_id,
            'user_id': self._user_id,
            'agent_name': self.agent_name,
            'current_task': self._current_task,
            'current_iteration': self._current_iteration,
            'max_iterations': self._max_iterations
        }