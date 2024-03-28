import subprocess

from src.processors.processor import Processor


class CompileProcessor(Processor):
    def __init__(
        self,
        compiler: str,
        compile_path: str,
        compile_output: str,
        compile_flags: list = [],
    ):
        super().__init__()
        self.compiler = compiler
        self.compile_path = compile_path
        self.compile_output = compile_output
        self.compile_flags = compile_flags

        self.module_args = {
            "compiler": compiler,
            "compile_path": compile_path,
            "compile_output": compile_output,
            "compile_flags": compile_flags,
        }

    def _process(self, obj):
        if self.compiler in ["gcc", "rustc"]:
            compile_command = [
                self.compiler,
                self.compile_path,
                "-o",
                self.compile_output,
            ] + self.compile_flags
        else:
            raise Exception(f"Compiler {self.compiler} not supported")

        # Compile
        result = subprocess.run(compile_command, capture_output=True, text=True)

        if result.returncode == 0:
            processed = obj
        else:
            raise Exception(f"{result.stderr}")
        return processed
