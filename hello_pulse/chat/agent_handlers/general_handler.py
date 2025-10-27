"""
Handler pour l'agent General
"""
from typing import Dict
from hello_pulse.chat.agent_handlers.base_handler import BaseAgentHandler
from hello_pulse.chat.utils.colors import Colors


class GeneralHandler(BaseAgentHandler):
    """Handler pour l'agent general avec ses commandes spécifiques"""
    
    @property
    def agent_name(self) -> str:
        return "General"
    
    @property
    def agent_emoji(self) -> str:
        return "🤖"
    
    def get_available_commands(self) -> Dict[str, str]:
        """Retourne les commandes spécifiques au general"""
        return {
            '/task': 'Définir une nouvelle tâche à accomplir',
            '/status': 'Afficher le statut de la tâche en cours',
            '/info': 'Afficher les informations de contexte'
        }
    
    async def handle_command(self, command: str) -> bool:
        """Traite les commandes spécifiques au general"""
        if command == '/task':
            self._set_task()
            return True
        
        elif command == '/status':
            self._show_status()
            return True
        
        elif command == '/info':
            await self.display_context()
            return True
        
        return False
    
    def _set_task(self):
        """Menu pour définir une nouvelle tâche"""
        print(f"\n{Colors.BOLD}📋 DÉFINIR UNE TÂCHE:{Colors.RESET}")
        print("Décrivez la tâche que l'agent doit accomplir :")
        print()
        
        task = input(f"{Colors.CYAN}Tâche: {Colors.RESET}").strip()
        
        if task:
            self.session.set_task(task)
            print(f"{Colors.GREEN}✅ Tâche enregistrée{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Tâche vide{Colors.RESET}")
    
    def _show_status(self):
        """Affiche le statut de la tâche en cours"""
        info = self.session.get_context_info()
        
        print(f"\n{Colors.BOLD}📊 STATUT DE LA TÂCHE:{Colors.RESET}")
        
        if info['current_task']:
            print(f"  Tâche : {Colors.CYAN}{info['current_task']}{Colors.RESET}")
            print(f"  Progression : {Colors.YELLOW}{info['current_iteration']}/{info['max_iterations']}{Colors.RESET} itérations")
        else:
            print(f"  {Colors.GRAY}Aucune tâche en cours{Colors.RESET}")
        print()
    
    async def display_context(self):
        """Affiche le contexte du general"""
        info = self.session.get_context_info()
        
        print(f"\n{Colors.BOLD}🤖 CONTEXTE GENERAL:{Colors.RESET}")
        print(f"  Session ID: {Colors.CYAN}{info['session_id']}{Colors.RESET}")
        print(f"  Utilisateur: {Colors.CYAN}{info['user_id']}{Colors.RESET}")
        
        if info['current_task']:
            print(f"  Tâche actuelle: {Colors.MAGENTA}{info['current_task']}{Colors.RESET}")
            print(f"  Itération: {Colors.YELLOW}{info['current_iteration']}/{info['max_iterations']}{Colors.RESET}")
        else:
            print(f"  {Colors.GRAY}Aucune tâche définie{Colors.RESET}")
        print()