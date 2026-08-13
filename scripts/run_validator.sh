#!/bin/bash
# Script de lancement du validator CATAR

echo "=== Lancement du Validator CATAR ==="

# Activation de l'environnement Python
source venv/bin/activate

# Exécution du validator
python3 validator/validator.py --validator.name catar-validator

echo "=== Validator CATAR arrêté ==="
