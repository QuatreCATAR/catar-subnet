# validator.py
# Validator CATAR minimal — structure de base pour Subnet Bittensor

import argparse
import logging
import bittensor as bt

# -----------------------------------------------------------------------------
# 01 — Configuration de base du validator
# -----------------------------------------------------------------------------

def get_config():
    parser = argparse.ArgumentParser()
    bt.wallet.add_args(parser)
    bt.subtensor.add_args(parser)
    bt.logging.add_args(parser)

    parser.add_argument(
        "--validator.name",
        type=str,
        default="catar-validator",
        help="Nom du validator CATAR."
    )

    config = bt.config(parser)
    bt.logging(config=config, logging_dir="logs")
    return config


# -----------------------------------------------------------------------------
# 02 — Classe ValidatorCATAR minimale
# -----------------------------------------------------------------------------

class ValidatorCATAR:
    """
    Validator CATAR minimal.
    Pour l’instant :
    - interroge les miners
    - reçoit une réponse
    - attribue un score simple
    """

    def __init__(self, config: bt.Config):
        self.config = config

        # Wallet (coldkey + hotkey)
        self.wallet = bt.wallet(config=self.config)

        # Subtensor (connexion au réseau)
        self.subtensor = bt.subtensor(config=self.config)

        logging.info("ValidatorCATAR initialisé.")

    # -------------------------------------------------------------------------
    # 03 — Logique minimale d’évaluation
    # -------------------------------------------------------------------------

    def forward(self):
        """
        Interroge un miner du réseau.
        Version minimale : envoie une requête simple et reçoit une réponse.
        """

        synapse = bt.Synapse()
        response = self.subtensor.query(
            wallet=self.wallet,
            synapse=synapse
        )

        logging.info(f"Réponse reçue du miner : {response.completion}")

        # Score minimal (placeholder)
        score = 1.0

        logging.info(f"Score attribué : {score}")
        return score

    # -------------------------------------------------------------------------
    # 04 — Boucle principale
    # -------------------------------------------------------------------------

    def run(self):
        logging.info("Démarrage du validator CATAR minimal...")

        try:
            while True:
                self.forward()
        except KeyboardInterrupt:
            logging.info("Arrêt du validator CATAR.")


# -----------------------------------------------------------------------------
# 05 — Entrée principale
# -----------------------------------------------------------------------------

def main():
    config = get_config()
    validator = ValidatorCATAR(config=config)
    validator.run()


if __name__ == "__main__":
    main()
