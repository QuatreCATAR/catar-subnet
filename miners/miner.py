# miner.py
# Miner CATAR minimal — structure de base pour Subnet Bittensor

import argparse
import logging
import bittensor as bt

# -----------------------------------------------------------------------------
# 01 — Configuration de base du miner
# -----------------------------------------------------------------------------

def get_config():
    parser = argparse.ArgumentParser()
    bt.axon.add_args(parser)
    bt.wallet.add_args(parser)
    bt.subtensor.add_args(parser)
    bt.logging.add_args(parser)

    parser.add_argument(
        "--miner.name",
        type=str,
        default="catar-miner",
        help="Nom du miner CATAR."
    )

    config = bt.config(parser)
    bt.logging(config=config, logging_dir="logs")
    return config


# -----------------------------------------------------------------------------
# 02 — Classe MinerCATAR minimale
# -----------------------------------------------------------------------------

class MinerCATAR:
    """
    Miner CATAR minimal.
    Pour l’instant :
    - se connecte au réseau Bittensor
    - expose un axon
    - répond avec un placeholder CATAR
    """

    def __init__(self, config: bt.Config):
        self.config = config

        # Wallet (coldkey + hotkey)
        self.wallet = bt.wallet(config=self.config)

        # Subtensor (connexion au réseau)
        self.subtensor = bt.subtensor(config=self.config)

        # Axon (serveur qui reçoit les requêtes des validateurs)
        self.axon = bt.axon(
            wallet=self.wallet,
            config=self.config,
        )

        # Enregistrement des callbacks
        self.axon.attach(
            forward_fn=self.forward,
            blacklist_fn=self.blacklist,
            priority_fn=self.priority,
        )

        logging.info("MinerCATAR initialisé.")

    # -------------------------------------------------------------------------
    # 03 — Logique minimale de réponse (placeholder CATAR)
    # -------------------------------------------------------------------------

    def forward(self, synapse: bt.Synapse) -> bt.Synapse:
        """
        Fonction appelée à chaque requête du validator.
        Version minimale : renvoie un message CATAR générique.
        Plus tard : intégration du Passage CATAR complet.
        """

        # Placeholder : réponse minimale
        synapse.completion = (
            "Réponse CATAR minimale : le Passage complet n’est pas encore implémenté, "
            "mais le miner est fonctionnel et prêt à intégrer le Corpus et la logique "
            "Test → Corpus → Contrôle → Correction → Analyse."
        )

        logging.debug(f"Réponse envoyée au validator: {synapse.completion}")
        return synapse

    # -------------------------------------------------------------------------
    # 04 — Blacklist et priorité (version minimale)
    # -------------------------------------------------------------------------

    def blacklist(self, synapse: bt.Synapse) -> bool:
        """
        Permet de refuser certaines requêtes.
        Version minimale : aucune requête n’est blacklistée.
        """
        return False

    def priority(self, synapse: bt.Synapse) -> float:
        """
        Permet de donner une priorité aux requêtes.
        Version minimale : priorité constante.
        """
        return 0.5

    # -------------------------------------------------------------------------
    # 05 — Boucle principale
    # -------------------------------------------------------------------------

    def run(self):
        """
        Lance l’axon et reste en écoute.
        """
        logging.info("Démarrage du miner CATAR minimal...")
        self.axon.start()
        logging.info("Axon en écoute. MinerCATAR opérationnel.")

        # Boucle infinie minimale
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logging.info("Arrêt du miner CATAR.")
            self.axon.stop()


# -----------------------------------------------------------------------------
# 06 — Entrée principale
# -----------------------------------------------------------------------------

def main():
    config = get_config()
    miner = MinerCATAR(config=config)
    miner.run()


if __name__ == "__main__":
    main()
