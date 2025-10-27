"""
Helper pour gérer les tools MCP dans config.yml

Permet d'ajouter, supprimer ou lister les tools MCP
pour chaque agent de manière programmatique.
"""
import yaml
from pathlib import Path
from typing import List, Optional


class ConfigToolsManager:
    """Gestionnaire des tools MCP dans config.yml"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialise le gestionnaire.
        
        Args:
            config_path: Chemin vers config.yml (par défaut: racine du projet)
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config.yml'
        
        self.config_path = config_path
        self._load_config()
    
    def _load_config(self):
        """Charge la configuration depuis le fichier YAML"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
    
    def _save_config(self):
        """Sauvegarde la configuration dans le fichier YAML"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def get_tools(self, agent_name: str) -> List[str]:
        """
        Récupère la liste des tools MCP pour un agent.
        
        Args:
            agent_name: Nom de l'agent (assistant, facilitator, studio)
            
        Returns:
            Liste des tools MCP configurés
        """
        agent_config = self.config.get('agents', {}).get(agent_name, {})
        return agent_config.get('tools_mcp', [])
    
    def add_tool(self, agent_name: str, tool_name: str) -> bool:
        """
        Ajoute un tool MCP à un agent.
        
        Args:
            agent_name: Nom de l'agent
            tool_name: Nom du tool à ajouter
            
        Returns:
            True si ajouté, False si déjà présent
        """
        tools = self.get_tools(agent_name)
        
        if tool_name in tools:
            return False
        
        tools.append(tool_name)
        
        # Mettre à jour la config
        if 'agents' not in self.config:
            self.config['agents'] = {}
        if agent_name not in self.config['agents']:
            self.config['agents'][agent_name] = {}
        
        self.config['agents'][agent_name]['tools_mcp'] = tools
        self._save_config()
        
        return True
    
    def remove_tool(self, agent_name: str, tool_name: str) -> bool:
        """
        Supprime un tool MCP d'un agent.
        
        Args:
            agent_name: Nom de l'agent
            tool_name: Nom du tool à supprimer
            
        Returns:
            True si supprimé, False si non présent
        """
        tools = self.get_tools(agent_name)
        
        if tool_name not in tools:
            return False
        
        tools.remove(tool_name)
        self.config['agents'][agent_name]['tools_mcp'] = tools
        self._save_config()
        
        return True
    
    def list_all_tools(self) -> dict:
        """
        Liste tous les tools MCP pour tous les agents.
        
        Returns:
            Dictionnaire {agent_name: [tools]}
        """
        result = {}
        agents = self.config.get('agents', {})
        
        for agent_name in agents.keys():
            result[agent_name] = self.get_tools(agent_name)
        
        return result


# Exemple d'utilisation
if __name__ == "__main__":
    manager = ConfigToolsManager()
    
    print("📋 Tools MCP par agent :")
    print()
    
    all_tools = manager.list_all_tools()
    for agent, tools in all_tools.items():
        print(f"  {agent}:")
        if tools:
            for tool in tools:
                print(f"    - {tool}")
        else:
            print("    (aucun)")
        print()
