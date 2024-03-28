import json

from src.processors.processor import Processor


class JsonProcessor(Processor):
    def __init__(self):
        super().__init__()

    def _process(self, obj):
        json_object = json.loads(obj)
        processed = str(json_object)
        return processed
