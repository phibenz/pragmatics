from src.evaluators.evaluator import Evaluator

from src.processors.run_file import RunFileProcessor


class RunFileEvaluator(Evaluator):
    def __init__(self, file_path: str, file_args: list, file_type: str, output: str):
        super().__init__()
        self.output = output
        self.run_file_processor = RunFileProcessor(file_path, file_args, file_type)
        self.module_args = {
            "file_path": file_path,
            "file_args": file_args,
            "file_type": file_type,
            "output": output,
        }

    def _evaluate(self, text) -> bool:
        output, success = self.run_file_processor(text)
        if not success:
            raise Exception(f"Error in RunFileProcessor: {output}")
        return output == self.output
