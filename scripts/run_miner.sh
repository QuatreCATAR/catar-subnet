#!/bin/bash
# Script de lancement du miner CATAR

echo "=== Lancement du Miner CATAR ==="

# Activation de l'environnement Python
source venv/bin/activate

# Exécution du miner
python3 miners/miner.py --miner.name catar-miner

echo "=== Miner CATAR arrêté ==="
