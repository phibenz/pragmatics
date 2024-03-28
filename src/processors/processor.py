import logging

logger = logging.getLogger(__name__)


class Processor:
    def __init__(self):
        self.module_type = "processor"
        self.module_name = str(self.__class__.__name__)
        self.module_input = None
        self.module_output = None
        self.module_success = None
        self.module_error = None
        self.module_args = {}

    def __call__(self, obj: str) -> tuple[str, bool]:
        self.module_input = str(obj)
        try:
            processed = self._process(obj)
            success = True
        except Exception as e:
            self.module_error = str(e)
            logger.error(f"Error in {self.module_type} {self.module_name}: {e}")
            processed = None
            success = False
        self.module_output = str(processed)
        self.module_success = success
        return processed, success

    def _process(self, obj: str) -> str:
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

    def set_module_type(self, module_type: str):
        self.module_type = module_type
