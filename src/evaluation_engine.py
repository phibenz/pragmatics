from src.evaluators.word import WordEvaluator
from src.evaluators.python_fn import PythonFnEvaluator
from src.evaluators.file import IsFileEvaluator
from src.evaluators.run_file import RunFileEvaluator
from src.utils import conditional_evaluation


class EvaluationEngine:
    def __init__(self, evaluators: list, condition: str = "and"):
        self.evaluator_infos = []
        self.evaluators = []
        self.evaluators_condition = condition

        for evaluator in evaluators:
            self.evaluators.append(self._get_evaluator(evaluator))

    def _get_evaluator(self, evaluator: dict):
        if not "condition" in evaluator:
            evaluator["condition"] = "and"
        # Select the evaluator based on the type
        if evaluator["type"] == "word":
            return WordEvaluator(evaluator["words"], evaluator["condition"])
        elif evaluator["type"] == "run-file":
            assert "file-path" in evaluator, "File path not found in evaluator"
            if not "file-args" in evaluator:
                evaluator["file-args"] = []
            assert "file-type" in evaluator, "File type not found in evaluator"
            assert "output" in evaluator, "Output not found in evaluator"
            return RunFileEvaluator(
                file_path=evaluator["file-path"],
                file_args=evaluator["file-args"],
                file_type=evaluator["file-type"],
                output=evaluator["output"],
            )
        elif evaluator["type"] == "python-fn":
            assert "fn-name" in evaluator, "Function name not found in evaluator"
            if not "args" in evaluator:
                evaluator["args"] = []
            assert "output" in evaluator, "Output not found in evaluator"
            return PythonFnEvaluator(
                fn_name=evaluator["fn-name"],
                fn_args=evaluator["args"],
                fn_output=evaluator["output"],
            )
        elif evaluator["type"] == "isfile":
            assert "file-paths" in evaluator, "File paths not found in evaluator"
            return IsFileEvaluator(
                file_paths=evaluator["file-paths"], condition=evaluator["condition"]
            )
        else:
            raise ValueError(f"Evaluator type {evaluator['type']} not supported")

    def __call__(self, obj):
        results = []
        success = True
        for evaluator in self.evaluators:
            result, success = evaluator(obj)
            results.append(result)
            evaluator_info = evaluator.info()
            self.evaluator_infos.append(evaluator_info)
            if not success:
                break
        final_result = conditional_evaluation(self.evaluators_condition, results)
        # TODO: Construct the final result info
        return final_result, success

    def info(self):
        return self.evaluator_infos
