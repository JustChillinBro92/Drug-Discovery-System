import time

from openai import OpenAI, APIError, APIConnectionError, RateLimitError

from config.config import settings


class OpenAIClient:
    def __init__(
        self,
        retry_attempts=3,
        backoff_factor=0.5,
        api_key=None
    ):
        if retry_attempts < 1:
            raise ValueError("retry_attempts must be at least 1")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = settings.OPENAI_MODEL
        self.retry_attempts = retry_attempts
        self.backoff_factor = backoff_factor

    def generate(
        self,
        prompt: str,
        system_instruction: str | None = None,
        temperature: float = 0.2,
        max_output_tokens: int = 512,
        json_mode: bool = False,
        reasoning_effort: str | None = None
    ) -> str:
        messages = []
        if system_instruction:
            messages.append({
                "role": "system",
                "content": system_instruction
            })
        messages.append({"role": "user", "content": prompt})

        request = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_output_tokens,
        }
        if reasoning_effort:
            request["reasoning_effort"] = reasoning_effort
        if json_mode:
            request["response_format"] = {"type": "json_object"}

        for attempt in range(self.retry_attempts):
            try:
                response = self.client.chat.completions.create(**request)
                return response.choices[0].message.content or ""
            except (APIError, APIConnectionError, RateLimitError) as error:
                status_code = getattr(error, "status_code", None)
                retryable = status_code in {429, 500, 502, 503, 504}
                if not retryable:
                    raise
                if attempt == self.retry_attempts - 1:
                    raise
                print(f"Groq API error: {error}")
                time.sleep(self.backoff_factor * (2 ** attempt))