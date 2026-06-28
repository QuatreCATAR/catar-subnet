# validator.py
# Validator CATAR — Passage + Correction réelle + Analyse réelle

import argparse
import logging
import bittensor as bt

# Import du Passage CATAR
from catar_core.passage_catar import PassageCATAR

# Import de la Correction réelle
from catar_core.correction import CorrectionCATAR

# Import de l’Analyse réelle
from catar_core.analysis import AnalyseCATAR


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
    - applique l’Analyse CATAR réelle
    - attribue un score global CATAR
    """

    def __init__(self, config: bt.Config):
        self.config = config

        # Passage CATAR (cohérence interne)
        self.passage = PassageCATAR()

        # Correction réelle
        self.correction_engine = CorrectionCATAR(
            correction_path=self.config.catar.correction
        )

        # Analyse réelle
        self.analysis_engine = AnalyseCATAR()

        # Wallet
        self.wallet = bt.wallet(config=self.config)

        # Subtensor
        self.subtensor = bt.subtensor(config=self.config)

        logging.info("ValidatorCATAR initialisé avec Correction + Analyse CATAR.")

    # -------------------------------------------------------------------------
    # 03 — Interrogation du miner + Correction + Analyse
    # -------------------------------------------------------------------------

    def forward(self):
        """
        Interroge un miner, reçoit le Passage CATAR,
        applique la Correction réelle,
        applique l’Analyse CATAR,
        attribue un score global.
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

        # Analyse réelle
        analysis_result = self.analysis_engine.analyse(miner_output)

        # Score global CATAR
        score_global = correction_result["score"] + analysis_result["score"]

        logging.info(f"Score CATAR global : {score_global}")

        return {
            "miner_output": miner_output,
            "score_correction": correction_result["score"],
            "score_analyse": analysis_result["score"],
            "score_global": score_global,
            "markers": correction_result["markers"],
            "analysis": analysis_result,
            "details": {
                "correction": correction_result,
                "analyse": analysis_result
            }
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
