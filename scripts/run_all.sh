#!/bin/bash
# Script de lancement du miner + validator en parallèle

echo "=== Lancement du Subnet CATAR (miner + validator) ==="

# Activation de l'environnement Python
source venv/bin/activate

# Lancement du miner en arrière-plan
python3 miners/miner.py --miner.name catar-miner &
MINER_PID=$!

# Lancement du validator en arrière-plan
python3 validator/validator.py --validator.name catar-validator &
VALIDATOR_PID=$!

echo "Miner PID : $MINER_PID"
echo "Validator PID : $VALIDATOR_PID"

echo "=== Subnet CATAR opérationnel ==="

# Attente de l'arrêt manuel
wait $MINER_PID
wait $VALIDATOR_PID
