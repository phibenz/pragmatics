from src.processors.run_file import RunFileProcessor
from src.processors.extract_code import ExtractCodeProcessor
from src.processors.write_to_file import WriteToFileProcessor
from src.processors.python import (
    PythonCompileProcessor,
    PythonRunProcessor,
)
from src.processors.base64 import Base64DecodeProcessor, Base64EncodeProcessor
from src.processors.bash_run import BashRunProcessor
from src.processors.compile import CompileProcessor
from src.processors.language_model import LangugageModelProcessor
from src.processors.json import JsonProcessor


class ProcessorEngine:
    def __init__(self, processors: list):
        self.processors = []
        self.processor_infos = []

        for processor in processors:
            self.processors.append(self._get_processor(processor))

    def set_module_type(self, module_type: str):
        for processor in self.processors:
            processor.set_module_type(module_type)

    def _get_processor(self, processor: dict):
        if processor["type"] == "extract-code":
            return ExtractCodeProcessor()
        elif processor["type"] == "write-to-file":
            assert "file-path" in processor, "File path not found in processor"
            if not "file-type" in processor:
                processor["file-type"] = None
            if not "option" in processor:
                processor["option"] = []
            return WriteToFileProcessor(
                file_path=processor["file-path"],
                file_type=processor["file-type"],
                option=processor["option"],
            )
        elif processor["type"] == "run-file":
            assert "file-path" in processor, "File path not found in processor"
            if not "file-args" in processor:
                processor["file-args"] = []
            assert "file-type" in processor, "File language not found in processor"
            return RunFileProcessor(
                file_path=processor["file-path"],
                file_args=processor["file-args"],
                file_type=processor["file-type"],
            )
        # Python processors
        elif processor["type"] == "python-run":
            return PythonRunProcessor()
        elif processor["type"] == "python-compile":
            assert "fn-name" in processor, "Function name not found in processor"
            return PythonCompileProcessor(processor["fn-name"])
        # Base64 processors
        elif processor["type"] == "base64-decode":
            return Base64DecodeProcessor()
        elif processor["type"] == "base64-encode":
            return Base64EncodeProcessor()
        # Bash processors
        elif processor["type"] == "bash-run":
            return BashRunProcessor()
        # C processors
        elif processor["type"] == "compile":
            assert "compiler" in processor, "Compiler not found in processor"
            assert "compile-path" in processor, "Compile path not found in processor"
            assert "compile-output" in processor, "Output not found in processor"
            if not "compile-flags" in processor:
                processor["compile-flags"] = []
            return CompileProcessor(
                compiler=processor["compiler"],
                compile_path=processor["compile-path"],
                compile_output=processor["compile-output"],
                compile_flags=processor["compile-flags"],
            )
        # LLM processor
        elif processor["type"] == "llm":
            assert "model" in processor, "Model not found in processor"
            assert "query" in processor, "Query not found in processor"
            return LangugageModelProcessor(processor["model"], processor["query"])
        # JSON processor
        elif processor["type"] == "json":
            return JsonProcessor()
        else:
            raise ValueError(f"Processor type {processor['type']} not supported")

    def __call__(self, obj):
        success = True
        for processor in self.processors:
            obj, success = processor(obj)
            processor_info = processor.info()
            self.processor_infos.append(processor_info)
            if not success:
                break
        return obj, success

    def info(self):
        return self.processor_infos
