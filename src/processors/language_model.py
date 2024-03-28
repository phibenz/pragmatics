import re

from src.processors.processor import Processor
from src.utils import get_model


class LangugageModelProcessor(Processor):
    def __init__(self, model: str, query: str):
        super().__init__()
        self.model = get_model(model)
        self.query = query
        self.pattern = r"(\{\{\s*ANSWER\s*\}\})"

        self.module_args = {"model": model, "query": query}

    def _process(self, obj):
        # Replace the variables
        obj = re.sub(self.pattern, obj, self.query)
        self.model.add_user_prompt(obj)
        processed = self.model.query()
        return processed
