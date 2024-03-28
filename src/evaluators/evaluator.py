import logging

logger = logging.getLogger(__name__)


class Evaluator:
    def __init__(self):
        self.module_type = "evaluator"
        self.module_name = str(self.__class__.__name__)
        self.module_input = None
        self.module_output = None
        self.module_success = None
        self.module_error = None
        self.module_args = {}

    def __call__(self, obj) -> tuple[bool, bool]:
        self.module_input = str(obj)
        try:
            success = self._evaluate(obj)
            module_success = True
        except Exception as e:
            self.module_error = str(e)
            logger.error(f"Error in {self.module_type} {self.module_name}: {e}")
            success = None
            module_success = False
        self.module_output = str(success)
        self.module_success = module_success
        return success, module_success

    def _evaluate(self, obj) -> bool:
        raise NotImplementedError

    def info(self) -> dict:
        return {
            "type": self.module_type,
            "name": self.module_name,
            "input": self.module_input,
            "output": self.module_output,
            "success": self.module_success,
            "error": self.module_error,
            "args": self.module_args,
        }
