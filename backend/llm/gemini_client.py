import time

from google import genai
from google.genai import errors

from config.config import settings


class GeminiClient:
    def __init__(
        self,
        retry_attempts=3,
        backoff_factor=0.5,
        api_key=None
    ):
        if retry_attempts < 1:
            raise ValueError("retry_attempts must be at least 1")

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = settings.GEMINI_MODEL
        self.retry_attempts = retry_attempts
        self.backoff_factor = backoff_factor


    def generate(
        self,
        prompt: str,
        config=None
    ) -> str:

        for attempt in range(self.retry_attempts):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=config
                )
                return response.text
            except errors.APIError as error:
                print(f"Gemini API status code: {error.code}")
                if (
                    error.code not in {429, 500, 502, 503, 504}
                    or attempt == self.retry_attempts - 1
                ):
                    raise
                print(
                    "Retrying Gemini API "
                    f"(attempt {attempt + 2}/{self.retry_attempts})"
                )
                time.sleep(self.backoff_factor * (2 ** attempt))

