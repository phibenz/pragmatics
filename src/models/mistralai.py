import mistralai
from mistralai.client import MistralClient
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type,
)

from src.models.language_model import LanguageModel


class MistralAIModel(LanguageModel):
    def __init__(self, model: str, api_key: str):
        super().__init__()
        self.model = model
        self.client = MistralClient(api_key=api_key)
        self.system_prompt = None
        self.prompts = []

        self.module_args = {"model": model, "api_key": "api-key-redacted"}

        self.temperature = 0.7
        self.max_tokens = None

    def set_temperature(self, temperature: float):
        self.temperature = temperature

    def set_max_tokens(self, max_tokens: int):
        self.max_tokens = max_tokens

    def _set_system_prompt(self, system_prompt: str):
        self.system_prompt = {"role": "system", "content": system_prompt}

    def _add_user_prompt(self, user_prompt: str):
        self.prompts.append({"role": "user", "content": user_prompt})

    def _add_assistant_prompt(self, assistant_prompt: str):
        self.prompts.append({"role": "assistant", "content": assistant_prompt})

    @retry(
        wait=wait_random_exponential(min=1, max=60),
        retry=retry_if_exception_type(mistralai.exceptions.MistralException),
        stop=stop_after_attempt(6),
    )
    def _query(self) -> str:
        # The system prompt is always the first message for openai
        if self.system_prompt is not None:
            messages = [self.system_prompt] + self.prompts
        else:
            messages = self.prompts

        model_response = self.client.chat(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        out = model_response.choices[0].message.content
        return out
