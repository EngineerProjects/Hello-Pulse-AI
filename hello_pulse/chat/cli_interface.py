"""
Interface CLI universelle pour Hello Pulse

Interface générique permettant d'utiliser différents agents :
- 💬 Assistant (réactif, Q&A + recherche web)
- 🎭 Facilitateur (proactif, monitoring sessions)
- 🤖 Studio (futur - recherche approfondie)
"""
import asyncio
from typing import Optional
from hello_pulse.chat.sessions.session_manager import SessionManager, AgentType
from hello_pulse.chat.utils import (
    Colors,
    print_banner,
    print_agent_selection,
    print_help,
    print_session_header,
    print_message,
    print_error,
    print_success,
    print_info,
    clear_screen
)


class UnifiedCLI:
    """Interface CLI unifiée pour tous les agents"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.debug_mode = False
        self.running = True
    
    def select_agent(self) -> Optional[AgentType]:
        """
        Affiche le menu de sélection d'agent et retourne le choix.
        
        Returns:
            Type d'agent choisi ou None pour quitter
        """
        print_agent_selection()
        
        choice = input(f"{Colors.CYAN}Choisir un agent (0-3): {Colors.RESET}").strip()
        
        agent_map = {
            '1': 'assistant',
            '2': 'facilitator',
            '3': 'studio'
        }
        
        if choice == '0':
            return None
        
        if choice in agent_map:
            return agent_map[choice]
        
        print_error("Choix invalide")
        return self.select_agent()
    
    async def handle_general_commands(self, command: str) -> bool:
        """
        Gère les commandes générales (communes à tous les agents).
        
        Args:
            command: Commande à traiter
            
        Returns:
            True si la session doit continuer, False pour quitter
        """
        if command == '/quit' or command == '/exit':
            self.running = False
            return False
        
        elif command == '/help':
            agent_type = self.session_manager.current_agent_type or 'unknown'
            print_help(agent_type)
            
            # Afficher aussi les commandes spécifiques de l'agent
            if self.session_manager.current_handler:
                handler = self.session_manager.current_handler
                print(f"\n{Colors.BOLD}{handler.agent_emoji} Commandes spécifiques - {handler.agent_name}:{Colors.RESET}")
                for cmd, desc in handler.get_available_commands().items():
                    print(f"  {Colors.YELLOW}{cmd}{Colors.RESET} - {desc}")
                print()
        
        elif command == '/switch':
            await self.switch_agent()
        
        elif command == '/new':
            await self.new_session()
        
        elif command == '/debug':
            self.debug_mode = not self.debug_mode
            status = "activé" if self.debug_mode else "désactivé"
            print_info(f"Mode debug {status}")
        
        elif command == '/history':
            self.show_history()
        
        elif command == '/stats':
            self.show_stats()
        
        elif command == '/clear':
            if self.session_manager.current_session:
                self.session_manager.current_session.clear_history()
                print_success("Historique effacé")
        
        else:
            return True  # Commande non reconnue, passer au handler de l'agent
        
        return True
    
    async def switch_agent(self):
        """Change d'agent en cours de session"""
        print_info("Changement d'agent...")
        agent_type = self.select_agent()
        
        if agent_type is None:
            return
        
        try:
            # Nettoyer l'ancienne session
            await self.session_manager.cleanup_current_session()
            
            session, handler = self.session_manager.switch_agent(agent_type)
            print_success(f"Agent changé vers: {handler.agent_emoji} {handler.agent_name}")
            print_session_header(handler.agent_name, session.session_id)
        except NotImplementedError as e:
            print_error(str(e))
    
    async def new_session(self):
        """Démarre une nouvelle session avec le même agent"""
        if not self.session_manager.current_agent_type:
            print_error("Aucun agent actif")
            return
        
        agent_type = self.session_manager.current_agent_type
        session, handler = self.session_manager.create_session(agent_type)
        print_success("Nouvelle session créée")
        print_session_header(handler.agent_name, session.session_id)
    
    def show_history(self):
        """Affiche l'historique de la conversation"""
        if not self.session_manager.current_session:
            print_error("Aucune session active")
            return
        
        history = self.session_manager.current_session.history
        
        if not history:
            print_info("Historique vide")
            return
        
        print(f"\n{Colors.BOLD}📜 HISTORIQUE DE LA CONVERSATION:{Colors.RESET}")
        for i, msg in enumerate(history, 1):
            role_str = "Vous" if msg.role == "user" else msg.agent_name or "Agent"
            timestamp = msg.timestamp.strftime("%H:%M:%S")
            print(f"\n{Colors.GRAY}[{i}] {timestamp}{Colors.RESET}")
            print(f"{Colors.BOLD}{role_str}:{Colors.RESET} {msg.content[:100]}...")
        print()
    
    def show_stats(self):
        """Affiche les statistiques de la session"""
        if not self.session_manager.current_session:
            print_error("Aucune session active")
            return
        
        session = self.session_manager.current_session
        handler = self.session_manager.current_handler
        
        print(f"\n{Colors.BOLD}📊 STATISTIQUES DE SESSION:{Colors.RESET}")
        print(f"  Agent: {handler.agent_emoji} {handler.agent_name}")
        print(f"  Session ID: {Colors.CYAN}{session.session_id}{Colors.RESET}")
        print(f"  Messages: {Colors.GREEN}{len(session.history)}{Colors.RESET}")
        print(f"  Logs: {Colors.YELLOW}{session.get_log_path()}{Colors.RESET}")
        print()
    
    async def chat_loop(self):
        """Boucle principale du chat"""
        session = self.session_manager.current_session
        handler = self.session_manager.current_handler
        
        if not session or not handler:
            print_error("Aucune session active")
            return
        
        print_session_header(handler.agent_name, session.session_id)
        print_info("Tapez '/help' pour voir les commandes disponibles\n")
        
        while self.running:
            try:
                # Demander l'input utilisateur
                user_input = input(f"{Colors.BOLD}{Colors.GREEN}Vous:{Colors.RESET} ").strip()
                
                if not user_input:
                    continue
                
                # Vérifier si c'est une commande
                if user_input.startswith('/'):
                    # Commandes générales
                    should_continue = await self.handle_general_commands(user_input)
                    
                    if not should_continue:
                        break
                    
                    # Si la commande n'a pas été traitée, essayer avec le handler de l'agent
                    if should_continue is True:
                        handled = await handler.handle_command(user_input)
                        if not handled:
                            print_error(f"Commande inconnue: {user_input}")
                    
                    continue
                
                # Sinon, c'est un message normal - envoyer à l'agent
                print(f"{Colors.BOLD}{Colors.CYAN}{handler.agent_name}:{Colors.RESET} ", end='', flush=True)
                
                response = await session.chat(user_input)
                
                # Afficher la réponse
                if response and hasattr(response, 'content'):
                    print(response.content)
                    
                    # Debug mode
                    if self.debug_mode and hasattr(response, 'data'):
                        print(f"\n{Colors.GRAY}[DEBUG] Response data: {response.data}{Colors.RESET}")
                else:
                    print(response)
                
                print()  # Ligne vide après chaque réponse
                
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Interruption détectée{Colors.RESET}")
                confirm = input("Voulez-vous vraiment quitter? (o/N): ").strip().lower()
                if confirm in ['o', 'oui', 'y', 'yes']:
                    break
            
            except Exception as e:
                print_error(f"Erreur: {e}")
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()
        
        # Nettoyer la session avant de quitter
        session = self.session_manager.current_session
        await self.session_manager.cleanup_current_session()
        
        # Afficher le chemin du fichier de logs
        if session:
            log_path = session.get_log_path()
            print_success(f"Session terminée!")
            print_info(f"📊 Logs sauvegardés: {log_path}")
        else:
            print_info("Session sauvegardée. Au revoir! 👋")
    
    async def run(self):
        """Point d'entrée principal du CLI"""
        clear_screen()
        print_banner()
        
        # Sélection de l'agent
        agent_type = self.select_agent()
        
        if agent_type is None:
            print_info("Au revoir! 👋")
            return
        
        # Créer la session
        try:
            session, handler = self.session_manager.create_session(agent_type)
            print_success(f"Session créée avec {handler.agent_emoji} {handler.agent_name}")
        except NotImplementedError as e:
            print_error(str(e))
            return
        
        # Lancer la boucle de chat
        await self.chat_loop()


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Point d'entrée du programme"""
    cli = UnifiedCLI()
    
    try:
        asyncio.run(cli.run())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Programme interrompu{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Erreur fatale: {e}{Colors.RESET}")


if __name__ == "__main__":
    main()
