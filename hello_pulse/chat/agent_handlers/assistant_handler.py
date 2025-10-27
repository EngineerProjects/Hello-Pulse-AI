"""
Handler pour l'agent Assistant
"""
from typing import Dict
from hello_pulse.chat.agent_handlers.base_handler import BaseAgentHandler
from hello_pulse.chat.utils.colors import Colors


class AssistantHandler(BaseAgentHandler):
    """Handler pour l'agent assistant avec ses commandes spécifiques"""
    
    @property
    def agent_name(self) -> str:
        return "Assistant"
    
    @property
    def agent_emoji(self) -> str:
        return "💬"
    
    def get_available_commands(self) -> Dict[str, str]:
        """Retourne les commandes spécifiques à l'assistant"""
        return {
            '/phase': 'Changer la phase de travail (divergence, convergence, etc.)',
            '/role': 'Changer votre rôle (participant, facilitateur, observateur)',
            '/info': 'Afficher les informations de contexte'
        }
    
    async def handle_command(self, command: str) -> bool:
        """Traite les commandes spécifiques à l'assistant"""
        if command == '/phase':
            self._change_phase()
            return True
        
        elif command == '/role':
            self._change_role()
            return True
        
        elif command == '/info':
            await self.display_context()
            return True
        
        return False
    
    def _change_phase(self):
        """Menu pour changer la phase"""
        print(f"\n{Colors.BOLD}📍 CHOISIR UNE PHASE:{Colors.RESET}")
        print(f"  {Colors.YELLOW}1{Colors.RESET} - Divergence (génération d'idées)")
        print(f"  {Colors.YELLOW}2{Colors.RESET} - Convergence (sélection, organisation)")
        print(f"  {Colors.YELLOW}3{Colors.RESET} - Priorisation (classement, décision)")
        print(f"  {Colors.YELLOW}4{Colors.RESET} - Prototypage (création, test)")
        print()
        
        choice = input(f"{Colors.CYAN}Choisir (1-4): {Colors.RESET}").strip()
        
        phases = {
            '1': 'divergence',
            '2': 'convergence',
            '3': 'priorisation',
            '4': 'prototypage'
        }
        
        if choice in phases:
            self.session.set_phase(phases[choice])
            print(f"{Colors.GREEN}✅ Phase changée vers: {phases[choice]}{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Choix invalide{Colors.RESET}")
    
    def _change_role(self):
        """Menu pour changer le rôle"""
        print(f"\n{Colors.BOLD}👤 CHOISIR UN RÔLE:{Colors.RESET}")
        print(f"  {Colors.YELLOW}1{Colors.RESET} - Participant")
        print(f"  {Colors.YELLOW}2{Colors.RESET} - Facilitateur")
        print(f"  {Colors.YELLOW}3{Colors.RESET} - Observateur")
        print()
        
        choice = input(f"{Colors.CYAN}Choisir (1-3): {Colors.RESET}").strip()
        
        roles = {
            '1': 'participant',
            '2': 'facilitateur',
            '3': 'observateur'
        }
        
        if choice in roles:
            self.session.set_user_role(roles[choice])
            print(f"{Colors.GREEN}✅ Rôle changé vers: {roles[choice]}{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Choix invalide{Colors.RESET}")
    
    async def display_context(self):
        """Affiche le contexte de l'assistant"""
        info = self.session.get_context_info()
        
        print(f"\n{Colors.BOLD}💬 CONTEXTE ASSISTANT:{Colors.RESET}")
        print(f"  Session ID: {Colors.CYAN}{info['session_id']}{Colors.RESET}")
        print(f"  Utilisateur: {Colors.CYAN}{info['user_id']}{Colors.RESET}")
        print(f"  Rôle: {Colors.MAGENTA}{info['user_role']}{Colors.RESET}")
        print(f"  Phase: {Colors.YELLOW}{info['session_phase']}{Colors.RESET}")
        print()
