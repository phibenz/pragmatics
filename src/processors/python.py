from io import StringIO
from contextlib import redirect_stdout

from src.processors.processor import Processor


class PythonRunProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.f = StringIO()

    def _process(self, obj):
        # Execute the function string within a namespace
        with redirect_stdout(self.f):
            exec(obj)
        processed = self.f.getvalue().strip()
        return processed


class PythonCompileProcessor(Processor):
    def __init__(self, fn_name):
        super().__init__()
        self.fn_name = fn_name
        self.module_args = [fn_name]
        self.fn_namespace = {}

    def _process(self, obj):
        # Execute the function string within a namespace
        exec(obj, self.fn_namespace)
        processed = self.fn_namespace.get(self.fn_name)
        if processed is None:
            raise ValueError(f"Function {self.fn_name} not found")
        return processed
