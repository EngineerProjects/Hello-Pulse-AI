"""
Agent General - Agent autonome multi-tools pour Hello Pulse

Cet agent peut travailler de manière autonome sur des tâches complexes
nécessitant plusieurs étapes et l'utilisation de multiples tools MCP.
"""
from hello_pulse.agents.general.agent import general_agent
from hello_pulse.agents.general.dependencies import GeneralDeps
from hello_pulse.agents.general.output import GeneralOutput

__all__ = ['general_agent', 'GeneralDeps', 'GeneralOutput']