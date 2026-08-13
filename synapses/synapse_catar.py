import bittensor as bt

class SynapseCATAR(bt.Synapse):
    """
    Synapse CATAR : forme standard des échanges entre validator et miner.
    Le Corpus brut n'est jamais transmis, seules les sections dérivées.
    """
    prompt: str = ""
    test: str = ""
    control: str = ""
    correction: str = ""
    analysis: str = ""

    def to_dict(self):
        return {
            "prompt": self.prompt,
            "test": self.test,
            "Control": self.control,
            "Correction": self.correction,
            "Analysis": self.analysis,
        }

