import subprocess
from src.processors.processor import Processor


class RunFileProcessor(Processor):
    def __init__(self, file_path: str, file_args: list, file_type: str):
        super().__init__()
        self.file_path = file_path
        self.file_args = file_args
        self.file_type = file_type

        self.module_args = {
            "file_path": file_path,
            "file_args": file_args,
            "file_type": file_type,
        }

    def _process(self, obj) -> bool:
        if self.file_type in ["c", "rust"]:
            fn_command = [self.file_path] + self.file_args
        elif self.file_type == "python":
            fn_command = ["python", self.file_path] + self.file_args
        elif self.file_type == "bash":
            fn_command = ["bash", self.file_path] + self.file_args
        else:
            raise ValueError(f"File type: {self.file_type} not supported")

        result = subprocess.run(fn_command, capture_output=True, text=True)

        # Check if the command executed successfully
        if result.returncode == 0:
            processed = result.stdout.strip()
        else:
            raise Exception(f"{result.stderr}")
        return processed
