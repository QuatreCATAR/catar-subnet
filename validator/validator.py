# validator.py
# Validator CATAR — Passage + Correction + Analyse + Compte-Rendu

import argparse
import logging
import bittensor as bt

# Import du Passage CATAR
from catar_core.passage_catar import PassageCATAR

# Import de la Correction réelle
from catar_core.correction import CorrectionCATAR

# Import de l’Analyse réelle
from catar_core.analysis import AnalyseCATAR

# Import du Compte-Rendu CATAR
from catar_core.compte_rendu import CompteRenduCATAR


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
    - reçoit le Passage CATAR
    - applique la Correction réelle
    - applique l’Analyse CATAR
    - génère un Compte-Rendu CATAR complet
    - attribue un score global CATAR
    """

    def __init__(self, config: bt.Config):
        self.config = config

        # Passage CATAR
        self.passage = PassageCATAR()

        # Correction réelle
        self.correction_engine = CorrectionCATAR(
            correction_path=self.config.catar.correction
        )

        # Analyse réelle
        self.analysis_engine = AnalyseCATAR()

        # Compte-Rendu CATAR
        self.cr_engine = CompteRenduCATAR()

        # Wallet
        self.wallet = bt.wallet(config=self.config)

        # Subtensor
        self.subtensor = bt.subtensor(config=self.config)

        logging.info("ValidatorCATAR initialisé avec Correction + Analyse + Compte-Rendu.")

    # -------------------------------------------------------------------------
    # 03 — Interrogation du miner + Correction + Analyse + Compte-Rendu
    # -------------------------------------------------------------------------

    def forward(self):
        """
        Interroge un miner, reçoit le Passage CATAR,
        applique la Correction réelle,
        applique l’Analyse CATAR,
        génère un Compte-Rendu CATAR,
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

        # Passage CATAR interne (pour cohérence du rapport)
        passage_result = {
            "test": "Entrée envoyée par le validator",
            "corpus": self.config.catar.corpus,
            "control": "Contrôle interne minimal",
            "correction": correction_result["score"],
            "analysis": analysis_result["score"]
        }

        # Compte-Rendu CATAR
        compte_rendu = self.cr_engine.generate(
            passage_result=passage_result,
            correction_result=correction_result,
            analysis_result=analysis_result
        )

        logging.info("Compte-Rendu CATAR généré.")

        return {
            "miner_output": miner_output,
            "score_correction": correction_result["score"],
            "score_analyse": analysis_result["score"],
            "score_global": score_global,
            "markers": correction_result["markers"],
            "analysis": analysis_result,
            "compte_rendu": compte_rendu
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
