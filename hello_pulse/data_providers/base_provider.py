"""
Interface de base pour les fournisseurs de données
"""
from abc import ABC, abstractmethod
from typing import Optional
from hello_pulse.models.schemas import SessionContext, MonitoringMetrics


class BaseDataProvider(ABC):
    """
    Interface abstraite pour tous les fournisseurs de données.
    
    Permet de découpler la source des données (mock, API, database)
    de la logique métier des agents et du chat.
    """
    
    @abstractmethod
    async def get_session_context(self) -> SessionContext:
        """
        Récupère le contexte complet de la session.
        
        Returns:
            SessionContext avec toutes les informations de session
        """
        pass
    
    @abstractmethod
    async def update_metrics(self) -> MonitoringMetrics:
        """
        Met à jour et retourne les métriques de monitoring.
        
        Cette méthode est appelée périodiquement (ex: toutes les 30s)
        pour rafraîchir les métriques de participation, énergie, etc.
        
        Returns:
            MonitoringMetrics mises à jour
        """
        pass
    
    @abstractmethod
    async def update_session_phase(self, new_phase: str) -> bool:
        """
        Change la phase de la session.
        
        Args:
            new_phase: Nouvelle phase ("divergence", "convergence", "priorisation")
            
        Returns:
            True si le changement a réussi
        """
        pass
    
    @abstractmethod
    async def add_idea(self, idea: str, user_id: str) -> bool:
        """
        Ajoute une nouvelle idée à la session.
        
        Args:
            idea: Texte de l'idée
            user_id: ID de l'utilisateur qui a proposé l'idée
            
        Returns:
            True si l'ajout a réussi
        """
        pass
    
    async def get_participants(self) -> list:
        """
        Récupère la liste des participants.
        
        Returns:
            Liste des participants avec leurs infos
        """
        context = await self.get_session_context()
        return context.participants
    
    async def get_current_metrics(self) -> MonitoringMetrics:
        """
        Récupère les métriques actuelles sans mise à jour.
        
        Returns:
            Métriques actuelles
        """
        context = await self.get_session_context()
        return context.metrics
