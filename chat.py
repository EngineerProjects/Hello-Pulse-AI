#!/usr/bin/env python3
"""
Script pour lancer l'interface de chat avec l'agent facilitateur
"""
from pathlib import Path
import sys
from dotenv import load_dotenv

load_dotenv('.env')

# Importer et lancer le CLI
from hello_pulse.chat.cli_interface import main

if __name__ == "__main__":
    main()
