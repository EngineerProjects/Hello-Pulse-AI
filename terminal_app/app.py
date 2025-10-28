#!/usr/bin/env python3
"""
Interface CLI (Application Terminal) pour Hello Pulse

Cette application est le "consommateur" de la bibliothèque hello_pulse.
Elle utilise rich pour un affichage en streaming (non-bloquant).
"""
import asyncio
import json
from typing import Optional, List

# Imports de Rich pour l'affichage
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.panel import Panel
from rich.text import Text

# Imports depuis le CLI (cette application)
from terminal_app.session_manager import SessionManager, AgentType
from terminal_app.cli_utils import (
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
from terminal_app.cli_utils.logger import SessionLogger, ToolCall

# Imports depuis le COEUR IA (la bibliothèque)
from hello_pulse.chat.chat_session import ChatMessage


class UnifiedCLI:
    """Interface CLI unifiée pour tous les agents"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.logger: Optional[SessionLogger] = None
        self.debug_mode = False
        self.running = True
        self.console = Console() # Console Rich
    
    def select_agent(self) -> Optional[AgentType]:
        """Affiche le menu de sélection d'agent et retourne le choix."""
        print_agent_selection()
        
        choice = input(f"{Colors.CYAN}Choisir un agent (0-3): {Colors.RESET}").strip()
        
        agent_map = {
            '1': 'assistant',
            '2': 'facilitator',
            '3': 'general'  
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
            True si la boucle de chat doit continuer, False pour quitter
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
        
        return True # On a traité une commande, on continue la boucle
    
    async def switch_agent(self):
        """Change d'agent en cours de session"""
        print_info("Changement d'agent...")
        agent_type = self.select_agent()
        
        if agent_type is None:
            return
        
        try:
            # Nettoyer l'ancienne session
            await self.session_manager.cleanup_current_session()
            
            session, handler, logger = self.session_manager.create_session(agent_type)
            self.logger = logger # Mettre à jour le logger
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
        session, handler, logger = self.session_manager.create_session(agent_type)
        self.logger = logger # Mettre à jour le logger
        print_success("Nouvelle session créée")
        print_session_header(handler.agent_name, session.session_id)
    
    def show_history(self):
        """Affiche l'historique de la conversation"""
        if not self.session_manager.current_session:
            print_error("Aucune session active")
            return
        
        history: List[ChatMessage] = self.session_manager.current_session.history
        
        if not history:
            print_info("Historique vide")
            return
        
        print(f"\n{Colors.BOLD}📜 HISTORIQUE DE LA CONVERSATION:{Colors.RESET}")
        for i, msg in enumerate(history, 1):
            role_str = "Vous" if msg.role == "user" else msg.agent_name or "Agent"
            timestamp = msg.timestamp.strftime("%H:%M:%S")
            print(f"\n{Colors.GRAY}[{i}] {timestamp}{Colors.RESET}")
            # Utiliser self.console.print pour gérer le markdown
            self.console.print(f"{Colors.BOLD}{role_str}:{Colors.RESET}")
            self.console.print(Markdown(msg.content))
        print()
    
    def show_stats(self):
        """Affiche les statistiques de la session"""
        if not self.session_manager.current_session or not self.logger:
            print_error("Aucune session active")
            return
        
        session = self.session_manager.current_session
        handler = self.session_manager.current_handler
        
        print(f"\n{Colors.BOLD}📊 STATISTIQUES DE SESSION:{Colors.RESET}")
        print(f"  Agent: {handler.agent_emoji} {handler.agent_name}")
        print(f"  Session ID: {Colors.CYAN}{session.session_id}{Colors.RESET}")
        print(f"  Messages: {Colors.GREEN}{len(session.history)}{Colors.RESET}")
        print(f"  Logs: {Colors.YELLOW}{self.logger.get_log_path()}{Colors.RESET}")
        print()

    async def stream_chat_response(self, user_input: str):
        """
        Gère l'échange de chat en streaming avec rich.live.
        """
        session = self.session_manager.current_session
        handler = self.session_manager.current_handler
        
        if not session or not handler or not self.logger:
            print_error("Erreur critique: session ou logger non initialisé.")
            return

        # Logger le message utilisateur
        self.logger.log_message(role='user', content=user_input)

        # Variables pour accumuler la sortie
        current_markdown_output = ""
        final_response_text = ""
        tool_calls_list: List[ToolCall] = []
        
        # Le renderable Rich
        live_display = Markdown(current_markdown_output, code_theme="monokai")
        
        try:
            with Live(live_display, console=self.console, refresh_per_second=15, vertical_overflow="visible") as live:
                
                # Affiche le nom de l'agent avant que le stream ne commence
                live.update(Text(f"{handler.agent_emoji} {handler.agent_name}...", style="bold cyan"))
                
                current_thought = ""
                
                async for event in session.stream_chat(user_input):
                    
                    # 1. Mise à jour du contenu
                    if event.name == 'text_delta':
                        delta = event.data.get('delta', '')
                        # Si on est après une pensée (thought) ou un outil,
                        # c'est la réponse finale.
                        current_markdown_output += delta
                        
                    elif event.name == 'tool_call':
                        tool_name = event.data['tool_name']
                        tool_args = event.data['args']
                        tool_call_id = event.data['tool_call_id']
                        
                        # Créer un objet ToolCall pour le logger
                        tool_call = ToolCall(tool_name=tool_name, arguments=tool_args)
                        tool_calls_list.append(tool_call)

                        # Afficher l'appel d'outil
                        tool_str = f"`{tool_name}({json.dumps(tool_args, indent=2)})`"
                        current_markdown_output += f"\n\n---\n**Tool Call:** {tool_str}\n"

                    elif event.name == 'tool_output':
                        output = str(event.data.get('output'))
                        
                        # Mettre à jour l'objet ToolCall avec le résultat
                        if tool_calls_list:
                            tool_calls_list[-1].result = output

                        # Afficher le résultat de l'outil (tronqué)
                        output_preview = (output[:400] + '...') if len(output) > 400 else output
                        current_markdown_output += f"\n**Tool Output:**\n```json\n{output_preview}\n```\n---\n"
                    
                    elif event.name == 'end':
                        # Le stream est terminé
                        final_response_text = session._extract_text_from_output(event.run_result.output)
                        
                        # Si la réponse finale est *différente* de ce qui a déjà été streamé
                        # (cas où l'agent ne fait que répondre sans ReAct)
                        if not current_markdown_output or self.debug_mode:
                             current_markdown_output = final_response_text
                        
                        # Logger la réponse finale de l'agent
                        self.logger.log_message(
                            role='agent',
                            content=final_response_text,
                            tool_calls=tool_calls_list,
                            metadata=event.run_result.output.model_dump() if hasattr(event.run_result.output, 'model_dump') else None
                        )
                        
                    elif event.name == 'error':
                        error_msg = event.data.get('error_message', 'Erreur inconnue')
                        current_markdown_output += f"\n\n---\n**ERREUR:**\n`{error_msg}`"
                        print_error(f"Erreur de streaming: {error_msg}")

                    # 2. Mettre à jour l'affichage Live
                    # Nous enveloppons le Markdown dans un Panel pour un meilleur contrôle visuel
                    live.update(
                        Panel(
                            Markdown(current_markdown_output, code_theme="monokai"),
                            title=f"{handler.agent_emoji} {handler.agent_name}",
                            title_align="left",
                            border_style="cyan"
                        )
                    )

        except Exception as e:
            print_error(f"Une erreur est survenue pendant le chat: {e}")
            if self.debug_mode:
                import traceback
                traceback.print_exc()

    async def run(self):
        """Point d'entrée principal et boucle de chat du CLI"""
        clear_screen()
        print_banner()
        
        # 1. Sélection de l'agent
        agent_type = self.select_agent()
        
        if agent_type is None:
            print_info("Au revoir! 👋")
            return
        
        # 2. Créer la session
        try:
            session, handler, logger = self.session_manager.create_session(agent_type)
            self.logger = logger
            print_success(f"Session créée avec {handler.agent_emoji} {handler.agent_name}")
            print_session_header(handler.agent_name, session.session_id)
            print_info("Tapez '/help' pour voir les commandes disponibles\n")
        except Exception as e:
            print_error(f"Erreur lors de la création de la session: {e}")
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            return
        
        # 3. Boucle principale
        while self.running:
            try:
                # Utiliser la console Rich pour l'input
                user_input = self.console.input(f"[bold green]Vous:[/bold green] ").strip()
                
                if not user_input:
                    continue
                
                # Gérer les commandes
                if user_input.startswith('/'):
                    # Commandes générales
                    should_continue = await self.handle_general_commands(user_input)
                    
                    if not self.running:
                        break # /quit a été appelé
                    
                    # Si non gérée, essayer les commandes spécifiques à l'agent
                    if should_continue:
                        handled = await handler.handle_command(user_input)
                        if not handled:
                            print_error(f"Commande inconnue: {user_input}")
                    
                    continue # Demander le prochain input
                
                # Envoyer le message (maintenant en streaming)
                await self.stream_chat_response(user_input)

            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Interruption détectée{Colors.RESET}")
                confirm = input("Voulez-vous vraiment quitter? (o/N): ").strip().lower()
                if confirm in ['o', 'oui', 'y', 'yes']:
                    self.running = False
            
            except Exception as e:
                print_error(f"Erreur fatale dans la boucle principale: {e}")
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()
        
        # 4. Nettoyage
        await self.session_manager.cleanup_current_session()
        
        # Afficher le chemin du fichier de logs
        if self.logger:
            log_path = self.logger.get_log_path()
            print_success(f"Session terminée!")
            print_info(f"📊 Logs sauvegardés: {log_path}")
        else:
            print_info("Session sauvegardée. Au revoir! 👋")

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
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()