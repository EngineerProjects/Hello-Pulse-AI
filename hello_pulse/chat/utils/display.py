"""
Fonctions d'affichage pour l'interface CLI
"""
import os
from .colors import Colors


def clear_screen():
    """Efface l'écran du terminal"""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_banner():
    """Affiche la bannière de bienvenue"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                                                          ║")
    print("║            🎯 HELLO PULSE - CHAT INTERFACE               ║")
    print("║              Agents IA Multi-Agents                      ║")
    print("║                                                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")


def print_agent_selection():
    """Affiche le menu de sélection d'agent"""
    print(f"\n{Colors.BOLD}🤖 CHOISIR UN AGENT:{Colors.RESET}")
    print(f"  {Colors.GREEN}1{Colors.RESET} - 💬 Assistant (réactif - Q&A + recherche web)")
    print(f"  {Colors.GREEN}2{Colors.RESET} - 🎭 Facilitateur (proactif - monitoring sessions)")
    print(f"  {Colors.GRAY}3{Colors.RESET} - 🤖 Studio (bientôt disponible)")
    print(f"  {Colors.RED}0{Colors.RESET} - ❌ Quitter")
    print()


def print_help(agent_type: str):
    """
    Affiche l'aide des commandes selon l'agent
    
    Args:
        agent_type: Type d'agent ('assistant', 'facilitator', 'studio')
    """
    print(f"\n{Colors.BOLD}📖 COMMANDES GÉNÉRALES:{Colors.RESET}")
    print(f"  {Colors.GREEN}/help{Colors.RESET}        - Afficher cette aide")
    print(f"  {Colors.GREEN}/history{Colors.RESET}     - Afficher l'historique de la conversation")
    print(f"  {Colors.GREEN}/stats{Colors.RESET}       - Afficher les statistiques de session")
    print(f"  {Colors.GREEN}/clear{Colors.RESET}       - Effacer l'historique de conversation")
    print(f"  {Colors.GREEN}/debug{Colors.RESET}       - Activer/désactiver le mode debug")
    print(f"  {Colors.GREEN}/switch{Colors.RESET}      - Changer d'agent")
    print(f"  {Colors.GREEN}/new{Colors.RESET}         - Démarrer une nouvelle session")
    print(f"  {Colors.GREEN}/quit{Colors.RESET}        - Quitter le chat")
    print()
    
    # Afficher l'aide spécifique à l'agent
    print(f"{Colors.BOLD}📖 COMMANDES SPÉCIFIQUES - {agent_type.upper()}:{Colors.RESET}")
    print(f"  {Colors.YELLOW}(Utilisez la commande de l'agent pour voir les commandes spécifiques){Colors.RESET}")
    print()


def print_session_header(agent_name: str, session_id: str):
    """
    Affiche l'en-tête de session
    
    Args:
        agent_name: Nom de l'agent actif
        session_id: ID de la session
    """
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}  Agent actif: {Colors.GREEN}{agent_name}{Colors.RESET}")
    print(f"{Colors.BOLD}  Session ID: {Colors.GRAY}{session_id}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")


def print_message(role: str, content: str, agent_name: str = None):
    """
    Affiche un message formaté
    
    Args:
        role: 'user' ou 'agent'
        content: Contenu du message
        agent_name: Nom de l'agent (optionnel)
    """
    if role == 'user':
        print(f"{Colors.BOLD}{Colors.GREEN}Vous:{Colors.RESET} {content}")
    else:
        prefix = f"{agent_name}" if agent_name else "Agent"
        print(f"{Colors.BOLD}{Colors.CYAN}{prefix}:{Colors.RESET} {content}")


def print_error(message: str):
    """Affiche un message d'erreur"""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")


def print_success(message: str):
    """Affiche un message de succès"""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")


def print_info(message: str):
    """Affiche un message d'information"""
    print(f"{Colors.CYAN}ℹ️  {message}{Colors.RESET}")


def print_warning(message: str):
    """Affiche un message d'avertissement"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")
