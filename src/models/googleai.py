import google.generativeai as genai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

from src.models.language_model import LanguageModel


class GoogleAIModel(LanguageModel):
    def __init__(self, model: str, api_key: str):
        super().__init__()
        genai.configure(api_key=api_key)
        self.model = model
        self.client = genai.GenerativeModel(model)
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
        self.system_prompt = system_prompt

    def _add_user_prompt(self, user_prompt: str):
        self.prompts.append({"role": "user", "parts": [user_prompt]})

    def _add_assistant_prompt(self, assistant_prompt: str):
        self.prompts.append({"role": "model", "parts": [assistant_prompt]})

    @retry(
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(6),
    )
    def _query(self) -> str:
        # The system prompt is always the first message for openai

        if self.system_prompt is not None:
            if len(self.prompts) > 0:
                self.prompts[0]["parts"] = [
                    self.system_prompt + " " + self.prompts[0]["parts"][0]
                ]
            else:
                self.prompts.append({"role": "user", "parts": [self.system_prompt]})

        messages = self.prompts

        model_response = self.client.generate_content(
            messages,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=self.max_tokens, temperature=self.temperature
            ),
        )
        out = model_response.text
        return out
