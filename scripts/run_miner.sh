#!/bin/bash
echo "=== Lancement du Miner CATAR ==="
cd "$(dirname "$0")/.."  # revient à la racine du projet
python3 -m miners.miner  # exécute le module proprement
echo "=== Miner CATAR arrêté ==="
