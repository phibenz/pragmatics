import os
import logging

from src.processors.processor import Processor

logger = logging.getLogger(__name__)


class WriteToFileProcessor(Processor):
    def __init__(self, file_path: str, file_type: str, option: dict):
        super().__init__()
        self.file_path = file_path
        self.file_type = file_type
        self.option = option
        self.module_args = {
            "file_path": self.file_path,
            "file_type": self.file_type,
            "option": self.option,
        }
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def _process(self, obj):
        if self.file_type == "c":
            if "replace-main" in self.option:
                obj = obj.replace("int main() {", "int old_main() {")

        with open(self.file_path, "w") as f:
            f.write(obj)
        return obj
