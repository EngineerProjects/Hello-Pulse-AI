"""
Agent Assistant pour Hello Pulse

Exporte l'agent assistant et ses dépendances.
"""
from hello_pulse.agents.assistant.agent import assistant_agent
from hello_pulse.agents.assistant.dependencies import AssistantDeps

__all__ = [
    'assistant_agent',
    'AssistantDeps',
]
