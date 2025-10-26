"""
Fournisseur de données simulées pour le développement et les tests
"""
import random
from typing import Optional
from datetime import datetime

from hello_pulse.models.schemas import SessionContext, MonitoringMetrics
from hello_pulse.data_providers.base_provider import BaseDataProvider


class MockDataProvider(BaseDataProvider):
    """
    Génère des données simulées pour le développement.
    
    Supporte deux modes :
    - random_mode=True : Génère des données aléatoires à chaque appel
    - random_mode=False : Retourne des données fixes prédéfinies
    
    Au démarrage, génère une équipe de taille aléatoire (3-10 membres par défaut)
    Les participants restent constants pendant la session, mais leurs métriques évoluent.
    """
    
    # Noms prédéfinis pour générer des participants
    FIRST_NAMES = [
        "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", 
        "Grace", "Henry", "Iris", "Jack", "Kate", "Leo",
        "Maria", "Noah", "Olivia", "Paul", "Quinn", "Rachel"
    ]
    
    EXPERTISES = [
        ["design", "UX"], 
        ["développement", "backend"],
        ["développement", "frontend"],
        ["business", "stratégie"],
        ["marketing", "communication"],
        ["data", "analytics"],
        ["product", "management"],
        ["recherche", "UX research"]
    ]
    
    def __init__(
        self, 
        session_id: str = "mock-session",
        random_mode: bool = True,
        config: Optional[dict] = None
    ):
        self.session_id = session_id
        self.random_mode = random_mode
        self.config = config or {}
        
        # Configuration depuis config.yml ou valeurs par défaut
        team_config = self.config.get('team_size', {})
        self.min_team_size = team_config.get('min', 3)
        self.max_team_size = team_config.get('max', 10)
        
        # État interne de la session
        self._phase = "divergence"
        self._ideas = [
            "Application mobile de productivité",
            "Plateforme de collaboration en temps réel",
            "Outil d'analyse de données visuelle"
        ]
        
        # Générer l'équipe au démarrage
        self._participants = self._generate_random_team()
        
        self._session_duration = 0  # En secondes
        self._last_update = datetime.now()
    
    def _generate_random_team(self) -> list:
        """
        Génère une équipe de taille aléatoire avec des participants uniques.
        
        Returns:
            Liste de participants avec id, name, expertise
        """
        team_size = random.randint(self.min_team_size, self.max_team_size)
        
        # Sélectionner des noms uniques
        selected_names = random.sample(self.FIRST_NAMES, team_size)
        
        participants = []
        for i, name in enumerate(selected_names):
            participants.append({
                "id": f"user{i+1}",
                "name": name,
                "expertise": random.choice(self.EXPERTISES)
            })
        
        return participants
    
    async def get_session_context(self) -> SessionContext:
        """Récupère le contexte de session avec métriques"""
        metrics = await self.update_metrics()
        
        return SessionContext(
            session_id=self.session_id,
            phase=self._phase,
            participants=self._participants,
            current_ideas=self._ideas,
            metrics=metrics
        )
    
    async def update_metrics(self) -> MonitoringMetrics:
        """
        Met à jour les métriques de monitoring.
        
        En mode random, génère des valeurs aléatoires.
        En mode fixe, retourne des valeurs prédéfinies.
        """
        # Calculer le temps écoulé depuis la dernière mise à jour
        now = datetime.now()
        elapsed = (now - self._last_update).total_seconds()
        self._session_duration += int(elapsed)
        self._last_update = now
        
        if self.random_mode:
            return self._generate_random_metrics()
        else:
            return self._generate_fixed_metrics()
    
    def _generate_random_metrics(self) -> MonitoringMetrics:
        """Génère des métriques aléatoires réalistes"""
        # Participation : distribution aléatoire qui somme à ~100%
        participation = {}
        total = 0
        for p in self._participants[:-1]:
            value = random.uniform(20, 45)
            participation[p['id']] = value
            total += value
        participation[self._participants[-1]['id']] = max(5, 100 - total)
        
        # Durées de silence : distribution réaliste
        silence = {}
        for p in self._participants:
            # 70% des participants : silence court (0-300s)
            # 30% des participants : silence long (300-1000s)
            if random.random() < 0.7:
                silence[p['id']] = random.randint(0, 300)
            else:
                silence[p['id']] = random.randint(300, 1000)
        
        # Énergie du groupe : varie selon la phase et la durée
        base_energy = 70.0
        if self._phase == "divergence":
            energy_level = base_energy + random.uniform(-15, 15)
        elif self._phase == "convergence":
            energy_level = base_energy + random.uniform(-10, 10)
        else:  # priorisation
            energy_level = base_energy + random.uniform(-20, 5)
        
        energy_level = max(0, min(100, energy_level))
        
        # Score d'alerte basé sur les métriques
        alert_score = self._calculate_alert_score(
            participation, silence, energy_level
        )
        
        return MonitoringMetrics(
            participation_rate=participation,
            silence_duration=silence,
            energy_level=energy_level,
            phase_duration=self._session_duration,
            total_ideas=len(self._ideas),
            alert_score=alert_score
        )
    
    def _generate_fixed_metrics(self) -> MonitoringMetrics:
        """Génère des métriques fixes pour tests reproductibles"""
        return MonitoringMetrics(
            participation_rate={
                "user1": 35.0,
                "user2": 40.0,
                "user3": 25.0
            },
            silence_duration={
                "user1": 120,
                "user2": 60,
                "user3": 300
            },
            energy_level=70.0,
            phase_duration=self._session_duration,
            total_ideas=len(self._ideas),
            alert_score=20
        )
    
    def _calculate_alert_score(
        self, 
        participation: dict,
        silence: dict,
        energy: float
    ) -> int:
        """
        Calcule un score d'alerte (0-100) basé sur les métriques.
        
        Score élevé = situation nécessitant intervention
        """
        score = 0
        
        # Participation déséquilibrée
        values = list(participation.values())
        if max(values) > 50:  # Quelqu'un domine
            score += 20
        if min(values) < 15:  # Quelqu'un très silencieux
            score += 25
        
        # Silence prolongé
        for duration in silence.values():
            if duration > 900:  # >15 minutes
                score += 30
            elif duration > 600:  # >10 minutes
                score += 15
        
        # Énergie basse
        if energy < 50:
            score += 20
        elif energy < 30:
            score += 35
        
        return min(100, score)
    
    async def update_session_phase(self, new_phase: str) -> bool:
        """Change la phase de la session"""
        if new_phase in ["divergence", "convergence", "priorisation"]:
            self._phase = new_phase
            return True
        return False
    
    async def add_idea(self, idea: str, user_id: str) -> bool:
        """Ajoute une nouvelle idée à la session"""
        self._ideas.append(idea)
        return True
    
    def reset_session(self):
        """Réinitialise la session (utile pour les tests)"""
        self._phase = "divergence"
        self._ideas = [
            "Application mobile de productivité",
            "Plateforme de collaboration en temps réel",
            "Outil d'analyse de données visuelle"
        ]
        self._session_duration = 0
        self._last_update = datetime.now()
