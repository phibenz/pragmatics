import os
from src.evaluators.evaluator import Evaluator
from src.utils import conditional_evaluation


class IsFileEvaluator(Evaluator):
    def __init__(self, file_paths: list, condition: str = "and"):
        super().__init__()
        self.file_paths = file_paths
        self.condition = condition
        self.module_args = {"file_paths": file_paths, "condition": condition}

    def _evaluate(self, obj) -> bool:
        matches = []
        for file_path in self.file_paths:
            if os.path.isfile(file_path):
                matches.append(True)
            else:
                matches.append(False)
        return conditional_evaluation(self.condition, matches)
