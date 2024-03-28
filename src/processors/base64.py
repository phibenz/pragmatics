import base64
from src.processors.processor import Processor


class Base64DecodeProcessor(Processor):
    def __init__(self):
        super().__init__()

    def _process(self, obj):
        processed = base64.b64decode(obj).decode("utf-8")
        return processed


class Base64EncodeProcessor(Processor):
    def __init__(self):
        super().__init__()

    def _process(self, obj):
        processed = base64.b64encode(obj.encode("utf-8")).decode("utf-8")
        return processed
