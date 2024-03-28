from src.evaluators.evaluator import Evaluator


class PythonFnEvaluator(Evaluator):
    def __init__(self, fn_name: str, fn_args: list, fn_output: str):
        super().__init__()
        self.fn_name = fn_name
        self.fn_args = fn_args
        self.fn_output = fn_output
        self.module_args = {
            "fn_name": fn_name,
            "fn_args": fn_args,
            "fn_output": fn_output,
        }

        if not isinstance(self.fn_args, list):
            self.fn_args = [self.fn_args]
        # Transform args if needed
        for idx, arg in enumerate(self.fn_args):
            if arg.startswith("eval:"):
                arg = eval(arg[5:])
                self.fn_args[idx] = arg

    def _evaluate(self, obj) -> bool:
        fn_out = obj(*self.fn_args)
        fn_out = str(fn_out)
        fn_result = fn_out == self.fn_output
        return fn_result
