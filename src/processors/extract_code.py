import re

from src.processors.processor import Processor


class ExtractCodeProcessor(Processor):
    def __init__(self):
        super().__init__()

    def _process(self, obj):
        processed = re.sub("```[a-z]*", "```", obj)
        if "```" in obj:
            processed = processed.split("```")[1]
        return processed
