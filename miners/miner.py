# miner.py
# Miner CATAR — version avec settings.yaml intégré

import argparse
import logging
import bittensor as bt
import yaml
import os

# Import Passage CATAR
from catar_core.passage_catar import PassageCATAR


# -----------------------------------------------------------------------------
# 01 — Chargement de settings.yaml
# -----------------------------------------------------------------------------

def load_settings():
    settings_path = os.path.join("config", "settings.yaml")
    with open(settings_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# -----------------------------------------------------------------------------
# 02 — Configuration du miner
# -----------------------------------------------------------------------------

def get_config():
    parser = argparse.ArgumentParser()
    bt.axon.add_args(parser)
    bt.wallet.add_args(parser)
    bt.subtensor.add_args(parser)
    bt.logging.add_args(parser)

    config = bt.config(parser)
    bt.logging(config=config, logging_dir="logs/miner")

    return config


# -----------------------------------------------------------------------------
# 03 — Classe MinerCATAR
# -----------------------------------------------------------------------------

class MinerCATAR:
    def __init__(self, config: bt.Config):
        self.config = config
        self.settings = load_settings()

        # Passage CATAR
        self.passage = PassageCATAR()

        # Wallet
        self.wallet = bt.wallet(config=self.config)

        # Subtensor
        self.subtensor = bt.subtensor(config=self.config)

        # Axon
        self.axon = bt.axon(
            wallet=self.wallet,
            config=self.config,
            port=self.settings["miner"]["axon_port"]
        )

        # Callbacks
        self.axon.attach(
            forward_fn=self.forward,
            blacklist_fn=self.blacklist,
            priority_fn=self.priority,
        )

        logging.info("MinerCATAR initialisé avec settings.yaml.")

    # -------------------------------------------------------------------------
    # 04 — Passage CATAR
    # -------------------------------------------------------------------------

    def forward(self, synapse: bt.Synapse) -> bt.Synapse:
        test_input = getattr(synapse, "prompt", "Entrée CATAR par défaut")

        result = self.passage.execute(
            test_input=test_input,
            corpus_path=self.settings["catar"]["corpus_path"]

        )

        synapse.completion = (
            f"Passage CATAR exécuté.\n"
            f"Test : {result['test']}\n"
            f"Corpus : {result['corpus']}\n"
            f"Contrôle : {result['control']}\n"
            f"Correction : {result['correction']}\n"
            f"Analyse : {result['analysis']}"
        )

        return synapse

    # -------------------------------------------------------------------------
    # 05 — Blacklist / Priorité
    # -------------------------------------------------------------------------

    def blacklist(self, synapse: bt.Synapse) -> bool:
        return False

    def priority(self, synapse: bt.Synapse) -> float:
        return 0.5

    # -------------------------------------------------------------------------
    # 06 — Boucle principale
    # -------------------------------------------------------------------------

    def run(self):
        logging.info("Démarrage du miner CATAR...")
        self.axon.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.axon.stop()


# -----------------------------------------------------------------------------
# 07 — Entrée principale
# -----------------------------------------------------------------------------

def main():
    config = get_config()
    miner = MinerCATAR(config=config)
    miner.run()


if __name__ == "__main__":
    main()
