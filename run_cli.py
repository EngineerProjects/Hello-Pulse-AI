#!/usr/bin/env python3
"""
Point d'entrée pour lancer l'application CLI (Terminal).
"""
import sys
from pathlib import Path
from dotenv import load_dotenv

# Assurer que la racine du projet est dans le path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

load_dotenv(project_root / '.env')

# Importer et lancer le CLI depuis terminal_app
from terminal_app.app import main

if __name__ == "__main__":
    main()