# validator.py
# Validator CATAR — Passage + Correction + Analyse + Compte-Rendu + settings.yaml

import argparse
import logging
import bittensor as bt
import yaml
import os

# Import modules CATAR
from catar_core.passage_catar import PassageCATAR
from catar_core.correction import CorrectionCATAR
from catar_core.analysis import AnalyseCATAR
from catar_core.compte_rendu import CompteRenduCATAR


# -----------------------------------------------------------------------------
# 01 — Chargement de settings.yaml
# -----------------------------------------------------------------------------

def load_settings():
    settings_path = os.path.join("config", "settings.yaml")
    with open(settings_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# -----------------------------------------------------------------------------
# 02 — Configuration du validator
# -----------------------------------------------------------------------------

def get_config():
    parser = argparse.ArgumentParser()
    bt.wallet.add_args(parser)
    bt.subtensor.add_args(parser)
    bt.logging.add_args(parser)

    config = bt.config(parser)
    bt.logging(config=config, logging_dir="logs/validator")

    return config


# -----------------------------------------------------------------------------
# 03 — Classe ValidatorCATAR
# -----------------------------------------------------------------------------

class ValidatorCATAR:
    def __init__(self, config: bt.Config):
        self.config = config
        self.settings = load_settings()

        # Passage CATAR
        self.passage = PassageCATAR()

        # Correction réelle
        self.correction_engine = CorrectionCATAR(
            correction_path=self.settings["catar"]["correction_path"]
        )

        # Analyse réelle
        self.analysis_engine = AnalyseCATAR()

        # Compte-Rendu CATAR
        self.cr_engine = CompteRenduCATAR()

        # Wallet
        self.wallet = bt.wallet(config=self.config)

        # Subtensor
        self.subtensor = bt.subtensor(config=self.config)

        logging.info("ValidatorCATAR initialisé avec settings.yaml.")

    # -------------------------------------------------------------------------
    # 04 — Passage + Correction + Analyse + Compte-Rendu
    # -------------------------------------------------------------------------

    def forward(self):
        synapse = bt.Synapse()
        response = self.subtensor.query(wallet=self.wallet, synapse=synapse)

        miner_output = response.completion

        correction_result = self.correction_engine.correct(miner_output)
        analysis_result = self.analysis_engine.analyse(miner_output)

        score_global = correction_result["score"] + analysis_result["score"]

        passage_result = {
            "test": "Entrée envoyée par le validator",
            "corpus": self.settings["catar"]["corpus_path"],
            "control": "Contrôle interne minimal",
            "correction": correction_result["score"],
            "analysis": analysis_result["score"]
        }

        compte_rendu = self.cr_engine.generate(
            passage_result=passage_result,
            correction_result=correction_result,
            analysis_result=analysis_result
        )

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
    # 05 — Boucle principale
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
# 06 — Entrée principale
# -----------------------------------------------------------------------------

def main():
    config = get_config()
    validator = ValidatorCATAR(config=config)
    validator.run()


if __name__ == "__main__":
    main()
