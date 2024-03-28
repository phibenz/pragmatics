import logging
import copy

logger = logging.getLogger(__name__)


class LanguageModel:
    def __init__(self):
        self.temperature = None
        self.max_tokens = None
        self.module_messages = []

        # Module metadata
        self.module_type = "language_model"
        self.module_name = str(self.__class__.__name__)
        self.module_input = []
        self.module_output = None
        self.module_success = None
        self.module_error = None
        self.module_args = {}

    def set_temperature(self, temperature: float):
        raise NotImplementedError

    def set_max_tokens(self, max_tokens: int):
        raise NotImplementedError

    def _set_system_prompt(self, system_prompt: str):
        raise NotImplementedError

    def _add_user_prompt(self, user_prompt: str):
        raise NotImplementedError

    def _add_assistant_prompt(self, assistant_prompt: str):
        raise NotImplementedError

    def _query(self) -> str:
        raise NotImplementedError

    def query(self):
        self.module_input = copy.deepcopy(self.module_messages)
        try:
            response = self._query()
            self.add_assistant_prompt(response)
            success = True
        except Exception as e:
            self.module_error = str(e)
            logger.error(f"Error in {self.module_type} {self.module_name}: {e}")
            success = False
            response = None
        self.module_output = response
        self.module_success = success
        return response, success

    def process_query(self, query):
        if "temperature" in query:
            self.set_temperature(query["temperature"])
        if "max_tokens" in query:
            self.set_max_tokens(query["max_tokens"])
        if "system" in query:
            self.set_system_prompt(query["system"])
        if "text" in query:
            self.add_user_prompt(query["text"])

        answer = self.query()
        return answer

    def set_system_prompt(self, system_prompt: str):
        if len(self.module_messages) == 0:
            self.module_messages.append({"role": "system", "content": system_prompt})
        elif self.module_messages[0]["role"] == "system":
            self.module_messages[0]["content"] = system_prompt
        else:
            self.module_messages.insert(0, {"role": "system", "content": system_prompt})

        self._set_system_prompt(system_prompt)

    def add_user_prompt(self, user_prompt: str):
        self.module_messages.append({"role": "user", "content": user_prompt})
        self._add_user_prompt(user_prompt)

    def add_assistant_prompt(self, assistant_prompt: str):
        self.module_messages.append({"role": "assistant", "content": assistant_prompt})
        self._add_assistant_prompt(assistant_prompt)

    def info(self) -> list:
        return [
            {
                "type": self.module_type,
                "name": self.module_name,
                "input": self.module_input,
                "output": self.module_output,
                "success": self.module_success,
                "error": self.module_error,
                "args": self.module_args,
            }
        ]
