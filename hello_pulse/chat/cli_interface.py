"""
Interface CLI pour tester l'agent facilitateur
"""
import asyncio
from datetime import datetime
from hello_pulse.chat.session_factory import create_facilitator_session
from hello_pulse.models.schemas import PostureType, MonitoringMetrics


class Colors:
    """Codes ANSI pour les couleurs dans le terminal"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'


def print_banner():
    """Affiche la bannière de bienvenue"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                                                          ║")
    print("║            🎯 HELLO PULSE - CHAT INTERFACE              ║")
    print("║              Agent Facilitateur IA                       ║")
    print("║                                                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")


def print_help():
    """Affiche l'aide des commandes"""
    print(f"\n{Colors.BOLD}📖 COMMANDES DISPONIBLES:{Colors.RESET}")
    print(f"  {Colors.GREEN}/help{Colors.RESET}        - Afficher cette aide")
    print(f"  {Colors.GREEN}/posture{Colors.RESET}     - Changer la posture de l'agent")
    print(f"  {Colors.GREEN}/history{Colors.RESET}     - Afficher l'historique")
    print(f"  {Colors.GREEN}/stats{Colors.RESET}       - Afficher les statistiques")
    print(f"  {Colors.GREEN}/context{Colors.RESET}     - Afficher le contexte de session")
    print(f"  {Colors.GREEN}/clear{Colors.RESET}       - Effacer l'historique")
    print(f"  {Colors.GREEN}/debug{Colors.RESET}       - Activer/désactiver le mode debug")
    print(f"  {Colors.GREEN}/quit{Colors.RESET}        - Quitter le chat")
    print()


def print_posture_menu():
    """Affiche le menu de sélection de posture"""
    print(f"\n{Colors.BOLD}🎭 CHOISIR UNE POSTURE:{Colors.RESET}")
    print(f"  {Colors.YELLOW}1{Colors.RESET} - Guide (encourageant, créatif)")
    print(f"  {Colors.YELLOW}2{Colors.RESET} - Provocateur (challenging, stimulant)")
    print(f"  {Colors.YELLOW}3{Colors.RESET} - Médiateur (apaisant, neutre)")
    print(f"  {Colors.YELLOW}4{Colors.RESET} - Timekeeper (organisé, orienté temps)")
    print()


async def print_context(session):
    """Affiche le contexte de la session"""
    ctx = await session.get_session_context()
    metrics = ctx.metrics
    
    print(f"\n{Colors.BOLD}🎯 CONTEXTE DE SESSION:{Colors.RESET}")
    print(f"  Session ID: {Colors.CYAN}{ctx.session_id}{Colors.RESET}")
    print(f"  Phase: {Colors.MAGENTA}{ctx.phase}{Colors.RESET}")
    print(f"  Posture actuelle: {Colors.YELLOW}{session.current_posture.value}{Colors.RESET}")
    print(f"\n  {Colors.BOLD}Participants:{Colors.RESET}")
    for p in ctx.participants:
        user_id = p['id']
        participation = metrics.participation_rate.get(user_id, 0)
        silence = metrics.silence_duration.get(user_id, 0)
        print(f"    • {p['name']} - {participation:.0f}% participation, "
              f"silence: {silence}s")
    
    print(f"\n  {Colors.BOLD}Métriques:{Colors.RESET}")
    print(f"    Énergie du groupe: {Colors.GREEN}{metrics.energy_level:.0f}%{Colors.RESET}")
    print(f"    Idées générées: {Colors.CYAN}{metrics.total_ideas}{Colors.RESET}")
    print(f"    Durée de phase: {Colors.YELLOW}{metrics.phase_duration}s{Colors.RESET}")
    print(f"    Score d'alerte: {Colors.RED}{metrics.alert_score}{Colors.RESET}")
    print()


async def handle_command(command: str, session, debug_mode: bool) -> tuple[bool, bool]:
    """
    Gère les commandes spéciales
    
    Returns:
        (should_continue, new_debug_mode)
    """
    if command == '/quit':
        print(f"{Colors.YELLOW}👋 Au revoir !{Colors.RESET}\n")
        return False, debug_mode
    
    elif command == '/help':
        print_help()
    
    elif command == '/posture':
        print_posture_menu()
        choice = input(f"{Colors.CYAN}Choisir (1-4): {Colors.RESET}")
        postures = [
            PostureType.GUIDE,
            PostureType.PROVOCATEUR,
            PostureType.MEDIATEUR,
            PostureType.TIMEKEEPER
        ]
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(postures):
                await session.change_posture(postures[idx])
            else:
                print(f"{Colors.RED}❌ Choix invalide{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}❌ Entrée invalide{Colors.RESET}")
    
    elif command == '/history':
        session.print_history()
    
    elif command == '/stats':
        stats = session.get_stats()
        print(f"\n{Colors.BOLD}📊 STATISTIQUES:{Colors.RESET}")
        for key, value in stats.items():
            print(f"  {key}: {Colors.CYAN}{value}{Colors.RESET}")
        print()
    
    elif command == '/context':
        await print_context(session)
    
    elif command == '/clear':
        session.clear_history()
    
    elif command == '/debug':
        debug_mode = not debug_mode
        status = "activé" if debug_mode else "désactivé"
        print(f"🐛 Mode debug {status}")
    
    else:
        print(f"{Colors.RED}❌ Commande inconnue. Tapez /help pour voir les commandes{Colors.RESET}")
    
    return True, debug_mode


def print_agent_response(response, debug_mode: bool = False):
    """Affiche la réponse de l'agent"""
    # Icône selon le type de message
    icon_map = {
        'public': '📢',
        'private': '🔒',
        'system': '⚙️'
    }
    icon = icon_map.get(response.message_type.value, '🤖')
    
    # Affichage principal
    print(f"\n{Colors.BOLD}{Colors.GREEN}{icon} Agent:{Colors.RESET}")
    print(f"  {response.message}\n")
    
    # Mode debug : affiche toutes les infos structurées
    if debug_mode:
        print(f"{Colors.BLUE}🐛 DEBUG INFO:{Colors.RESET}")
        print(f"  Message Type: {response.message_type.value}")
        print(f"  Posture: {response.current_posture.value}")
        if response.intervention_type:
            print(f"  Intervention: {response.intervention_type.value}")
        if response.target_user_id:
            print(f"  Cible: {response.target_user_id}")
        print()


async def chat_loop():
    """Boucle principale du chat"""
    print_banner()
    print(f"{Colors.CYAN}💡 Tapez /help pour voir les commandes disponibles{Colors.RESET}\n")
    
    # Créer une session de chat avec la factory
    session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    debug_mode = False
    
    session = create_facilitator_session(session_id=session_id)
    
    async with session:
        print(f"✅ Session démarrée : {Colors.CYAN}{session_id}{Colors.RESET}")
        print(f"🎭 Posture initiale : {Colors.YELLOW}{session.current_posture.value}{Colors.RESET}\n")
        
        running = True
        while running:
            try:
                # Prompt utilisateur
                user_input = input(f"{Colors.BOLD}{Colors.BLUE}Vous > {Colors.RESET}").strip()
                
                # Ignorer les entrées vides
                if not user_input:
                    continue
                
                # Gérer les commandes
                if user_input.startswith('/'):
                    running, debug_mode = await handle_command(user_input, session, debug_mode)
                    continue
                
                # Envoyer le message à l'agent
                print(f"{Colors.YELLOW}⏳ Agent en train de réfléchir...{Colors.RESET}", end='\r')
                
                try:
                    response = await session.send_message(user_input)
                    print(" " * 50, end='\r')  # Effacer le message de chargement
                    print_agent_response(response, debug_mode)
                    
                except Exception as e:
                    print(" " * 50, end='\r')
                    print(f"\n{Colors.RED}❌ Erreur : {e}{Colors.RESET}\n")
            
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}🛑 Interruption détectée{Colors.RESET}")
                confirm = input(f"Voulez-vous vraiment quitter ? (o/n) : ").lower()
                if confirm == 'o':
                    print(f"{Colors.YELLOW}👋 Au revoir !{Colors.RESET}\n")
                    break
            
            except EOFError:
                # Ctrl+D pressé
                print(f"\n{Colors.YELLOW}👋 Au revoir !{Colors.RESET}\n")
                break


def main():
    """Point d'entrée principal"""
    try:
        asyncio.run(chat_loop())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Au revoir !{Colors.RESET}\n")


if __name__ == "__main__":
    main()
