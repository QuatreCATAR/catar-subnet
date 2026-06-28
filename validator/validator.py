# validator.py
# Validator CATAR — version avec Correction réelle intégrée

import argparse
import logging
import bittensor as bt

# Import du Passage CATAR
from catar_core.passage_catar import PassageCATAR

# Import de la Correction réelle
from catar_core.correction import CorrectionCATAR


# -----------------------------------------------------------------------------
# 01 — Configuration du validator
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

    parser.add_argument(
        "--catar.corpus",
        type=str,
        default="corpus/corpus_catar.txt",
        help="Chemin vers le Corpus CATAR."
    )

    parser.add_argument(
        "--catar.correction",
        type=str,
        default="corpus/Correction.md",
        help="Chemin vers la Correction CATAR."
    )

    config = bt.config(parser)
    bt.logging(config=config, logging_dir="logs")
    return config


# -----------------------------------------------------------------------------
# 02 — Classe ValidatorCATAR
# -----------------------------------------------------------------------------

class ValidatorCATAR:
    """
    Validator CATAR :
    - interroge les miners
    - reçoit le Passage CATAR exécuté
    - applique la Correction réelle
    - attribue un score CATAR
    """

    def __init__(self, config: bt.Config):
        self.config = config

        # Passage CATAR (pour cohérence interne)
        self.passage = PassageCATAR()

        # Correction CATAR réelle
        self.correction_engine = CorrectionCATAR(
            correction_path=self.config.catar.correction
        )

        # Wallet
        self.wallet = bt.wallet(config=self.config)

        # Subtensor
        self.subtensor = bt.subtensor(config=self.config)

        logging.info("ValidatorCATAR initialisé avec Correction réelle.")

    # -------------------------------------------------------------------------
    # 03 — Interrogation du miner + Correction réelle
    # -------------------------------------------------------------------------

    def forward(self):
        """
        Interroge un miner, reçoit le Passage CATAR,
        applique la Correction réelle, attribue un score.
        """

        synapse = bt.Synapse()
        response = self.subtensor.query(
            wallet=self.wallet,
            synapse=synapse
        )

        miner_output = response.completion
        logging.info(f"Réponse reçue du miner : {miner_output}")

        # Correction réelle
        correction_result = self.correction_engine.correct(miner_output)

        # Score CATAR réel
        score = correction_result.get("score", 0.0)
        markers = correction_result.get("markers", [])

        logging.info(f"Score CATAR attribué : {score}")
        logging.info(f"Invariants détectés : {markers}")

        return {
            "miner_output": miner_output,
            "score": score,
            "markers": markers,
            "details": correction_result
        }

    # -------------------------------------------------------------------------
    # 04 — Boucle principale
    # -------------------------------------------------------------------------

    def run(self):
        logging.info("Démarrage du validator CATAR...")

        try:
            while True:
                result = self.forward()
                logging.debug(result)
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
