from .stability_test import run_stability_test
from .corpus_exposure import expose_corpus
from .comprehension_test import run_comprehension_test

def evaluate_model(model) -> dict:
    """
    Pipeline complet en 4 étapes :
    1. Test de stabilité initiale
    2. Exposition au Corpus
    3. Test de compréhension
    4. Test de stabilité finale
    """
    initial = run_stability_test(model("Bonjour"))
    corpus = expose_corpus()
    comprehension = run_comprehension_test(model(corpus))
    final = run_stability_test(model("Fin"))

    return {
        "initial_stability": initial,
        "comprehension": comprehension,
        "final_stability": final
    }

