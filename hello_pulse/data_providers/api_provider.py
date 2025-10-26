"""
Fournisseur de données via API REST (pour production)
"""
import httpx
from typing import Optional

from hello_pulse.models.schemas import SessionContext, MonitoringMetrics
from hello_pulse.data_providers.base_provider import BaseDataProvider


class APIDataProvider(BaseDataProvider):
    """
    Récupère les données depuis l'API REST de Hello Pulse.
    
    Cette classe sera utilisée en production pour récupérer les vraies
    données de session depuis le backend.
    
    Note: Skeleton pour le futur - à implémenter quand l'API sera prête
    """
    
    def __init__(
        self,
        base_url: str,
        session_id: str,
        api_key: Optional[str] = None,
        timeout: int = 10
    ):
        self.base_url = base_url.rstrip('/')
        self.session_id = session_id
        self.api_key = api_key
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _ensure_client(self):
        """Crée le client HTTP si nécessaire"""
        if self._client is None:
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout
            )
    
    async def close(self):
        """Ferme le client HTTP"""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def get_session_context(self) -> SessionContext:
        """
        Récupère le contexte de session depuis l'API.
        
        GET /api/sessions/{session_id}/context
        """
        await self._ensure_client()
        
        # TODO: Implémenter l'appel API réel
        response = await self._client.get(f'/api/sessions/{self.session_id}/context')
        response.raise_for_status()
        
        data = response.json()
        return SessionContext(**data)
    
    async def update_metrics(self) -> MonitoringMetrics:
        """
        Met à jour et récupère les métriques depuis l'API.
        
        POST /api/sessions/{session_id}/metrics/refresh
        """
        await self._ensure_client()
        
        # TODO: Implémenter l'appel API réel
        response = await self._client.post(
            f'/api/sessions/{self.session_id}/metrics/refresh'
        )
        response.raise_for_status()
        
        data = response.json()
        return MonitoringMetrics(**data)
    
    async def update_session_phase(self, new_phase: str) -> bool:
        """
        Change la phase de la session via l'API.
        
        PATCH /api/sessions/{session_id}/phase
        """
        await self._ensure_client()
        
        try:
            response = await self._client.patch(
                f'/api/sessions/{self.session_id}/phase',
                json={'phase': new_phase}
            )
            response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False
    
    async def add_idea(self, idea: str, user_id: str) -> bool:
        """
        Ajoute une idée via l'API.
        
        POST /api/sessions/{session_id}/ideas
        """
        await self._ensure_client()
        
        try:
            response = await self._client.post(
                f'/api/sessions/{self.session_id}/ideas',
                json={'idea': idea, 'user_id': user_id}
            )
            response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False
    
    async def __aenter__(self):
        """Context manager entry"""
        await self._ensure_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.close()
