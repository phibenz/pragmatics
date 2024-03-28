import subprocess

from src.processors.processor import Processor


class BashRunProcessor(Processor):
    def __init__(self):
        super().__init__()

    def _process(self, obj: str) -> str:
        # Run the bash command
        result = subprocess.run(obj, shell=True, capture_output=True, text=True)
        # Check if the command executed successfully
        if result.returncode == 0:
            processed = result.stdout.strip()
        else:
            raise Exception(f"{result.stderr}")
        return processed
