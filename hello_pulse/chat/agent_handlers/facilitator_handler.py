"""
Handler pour l'agent Facilitateur
"""
from typing import Dict
from hello_pulse.chat.agent_handlers.base_handler import BaseAgentHandler
from hello_pulse.chat.utils.colors import Colors
from hello_pulse.models.schemas import PostureType


class FacilitatorHandler(BaseAgentHandler):
    """Handler pour l'agent facilitateur avec ses commandes spécifiques"""
    
    @property
    def agent_name(self) -> str:
        return "Facilitateur"
    
    @property
    def agent_emoji(self) -> str:
        return "🎭"
    
    def get_available_commands(self) -> Dict[str, str]:
        """Retourne les commandes spécifiques au facilitateur"""
        return {
            '/posture': 'Changer la posture de l\'agent (Guide, Provocateur, etc.)',
            '/context': 'Afficher le contexte complet de la session',
            '/metrics': 'Afficher les métriques de la session'
        }
    
    async def handle_command(self, command: str) -> bool:
        """Traite les commandes spécifiques au facilitateur"""
        if command == '/posture':
            await self._change_posture()
            return True
        
        elif command == '/context':
            await self.display_context()
            return True
        
        elif command == '/metrics':
            await self._display_metrics()
            return True
        
        return False
    
    async def _change_posture(self):
        """Menu pour changer la posture"""
        print(f"\n{Colors.BOLD}🎭 CHOISIR UNE POSTURE:{Colors.RESET}")
        print(f"  {Colors.YELLOW}1{Colors.RESET} - Guide (encourageant, créatif)")
        print(f"  {Colors.YELLOW}2{Colors.RESET} - Provocateur (challenging, stimulant)")
        print(f"  {Colors.YELLOW}3{Colors.RESET} - Médiateur (apaisant, neutre)")
        print(f"  {Colors.YELLOW}4{Colors.RESET} - Timekeeper (organisé, orienté temps)")
        print()
        
        choice = input(f"{Colors.CYAN}Choisir (1-4): {Colors.RESET}").strip()
        
        postures = {
            '1': PostureType.GUIDE,
            '2': PostureType.PROVOCATEUR,
            '3': PostureType.MEDIATEUR,
            '4': PostureType.TIMEKEEPER
        }
        
        if choice in postures:
            await self.session.change_posture(postures[choice])
            print(f"{Colors.GREEN}✅ Posture changée vers: {postures[choice].value}{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Choix invalide{Colors.RESET}")
    
    async def display_context(self):
        """Affiche le contexte complet du facilitateur"""
        try:
            ctx = await self.session.get_session_context()
            metrics = ctx.metrics
            
            print(f"\n{Colors.BOLD}🎯 CONTEXTE DE SESSION FACILITATEUR:{Colors.RESET}")
            print(f"  Session ID: {Colors.CYAN}{ctx.session_id}{Colors.RESET}")
            print(f"  Phase: {Colors.MAGENTA}{ctx.phase}{Colors.RESET}")
            print(f"  Posture actuelle: {Colors.YELLOW}{self.session.current_posture.value}{Colors.RESET}")
            
            print(f"\n  {Colors.BOLD}Participants:{Colors.RESET}")
            for p in ctx.participants:
                user_id = p['id']
                participation = metrics.participation_rate.get(user_id, 0)
                silence = metrics.silence_duration.get(user_id, 0)
                print(f"    • {p['name']} - {participation:.0f}% participation, "
                      f"silence: {silence}s")
            
            await self._display_metrics()
            
        except Exception as e:
            print(f"{Colors.RED}❌ Erreur lors de la récupération du contexte: {e}{Colors.RESET}")
    
    async def _display_metrics(self):
        """Affiche les métriques de la session"""
        try:
            ctx = await self.session.get_session_context()
            metrics = ctx.metrics
            
            print(f"\n  {Colors.BOLD}📊 Métriques:{Colors.RESET}")
            print(f"    Énergie du groupe: {Colors.GREEN}{metrics.energy_level:.0f}%{Colors.RESET}")
            print(f"    Idées générées: {Colors.CYAN}{metrics.total_ideas}{Colors.RESET}")
            print(f"    Durée de phase: {Colors.YELLOW}{metrics.phase_duration}s{Colors.RESET}")
            print(f"    Score d'alerte: {Colors.RED}{metrics.alert_score}{Colors.RESET}")
            print()
        except Exception as e:
            print(f"{Colors.RED}❌ Erreur lors de la récupération des métriques: {e}{Colors.RESET}")
