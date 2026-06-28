# miner.py
# Miner CATAR — version avec PassageCATAR intégré

import argparse
import logging
import bittensor as bt

# Import du Passage CATAR
from catar_core.passage_catar import PassageCATAR

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

    parser.add_argument(
        "--catar.corpus",
        type=str,
        default="corpus/corpus_catar.txt",
        help="Chemin vers le Corpus CATAR."
    )

    config = bt.config(parser)
    bt.logging(config=config, logging_dir="logs")
    return config


# -----------------------------------------------------------------------------
# 02 — Classe MinerCATAR avec PassageCATAR
# -----------------------------------------------------------------------------

class MinerCATAR:
    """
    Miner CATAR :
    - se connecte au réseau Bittensor
    - expose un axon
    - exécute le Passage CATAR complet
    """

    def __init__(self, config: bt.Config):
        self.config = config

        # Passage CATAR
        self.passage = PassageCATAR()

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

        logging.info("MinerCATAR initialisé avec PassageCATAR.")

    # -------------------------------------------------------------------------
    # 03 — Logique CATAR : exécution du Passage
    # -------------------------------------------------------------------------

    def forward(self, synapse: bt.Synapse) -> bt.Synapse:
        """
        Fonction appelée à chaque requête du validator.
        Exécute le Passage CATAR complet.
        """

        # Entrée envoyée par le validator
        test_input = synapse.prompt if hasattr(synapse, "prompt") else "Entrée CATAR par défaut"

        # Exécution du Passage CATAR
        result = self.passage.execute(
            test_input=test_input,
            corpus_path=self.config.catar.corpus
        )

        # Réponse envoyée au validator
        synapse.completion = (
            f"Passage CATAR exécuté.\n"
            f"Test : {result['test']}\n"
            f"Corpus : {result['corpus']}\n"
            f"Contrôle : {result['control']}\n"
            f"Correction : {result['correction']}\n"
            f"Analyse : {result['analysis']}"
        )

        logging.debug(f"Réponse CATAR envoyée : {synapse.completion}")
        return synapse

    # -------------------------------------------------------------------------
    # 04 — Blacklist et priorité
    # -------------------------------------------------------------------------

    def blacklist(self, synapse: bt.Synapse) -> bool:
        return False

    def priority(self, synapse: bt.Synapse) -> float:
        return 0.5

    # -------------------------------------------------------------------------
    # 05 — Boucle principale
    # -------------------------------------------------------------------------

    def run(self):
        logging.info("Démarrage du miner CATAR...")
        self.axon.start()
        logging.info("Axon en écoute. MinerCATAR opérationnel.")

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
