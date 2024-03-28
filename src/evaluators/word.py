from src.evaluators.evaluator import Evaluator
from src.utils import conditional_evaluation


class WordEvaluator(Evaluator):
    def __init__(self, patterns: list, condition: str = "and"):
        super().__init__()
        self.patterns = patterns
        self.condition = condition
        self.module_args = {"patterns": patterns, "condition": condition}

    def _evaluate(self, obj) -> bool:
        matches = []
        for pattern in self.patterns:
            if pattern in obj:
                matches.append(True)
            else:
                matches.append(False)
        return conditional_evaluation(self.condition, matches)
