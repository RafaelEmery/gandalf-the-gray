import requests
import json
import traceback
from typing import Any
from .settings import settings
from rich import print


class OllamaClient:
    def __init__(
        self,
        base_url: str = settings.OLLAMA_URL,
        model: str = settings.OLLAMA_MODEL,
        timeout: int = settings.OLLAMA_TIMEOUT,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate(
        self, prompt: str, max_tokens: int = 512, temperature: float = 0.0
    ) -> str:
        """Calls local Ollama model via HTTP API (assumes ollama server running)."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            return handle_response(data)
        except Exception as e:
            print(
                f"[bold red] Error communicating with Ollama API {self.base_url}: [/bold red]"
            )
            traceback.print_exc()

            raise e


def handle_response(data: dict) -> Any:
    """
    Process the response from Ollama if needed.

    Ollama may stream; here we assume final result is in 'text' or 'response'
    """
    if isinstance(data, dict) and "text" in data:
        return data["text"]
    if isinstance(data, dict) and "response" in data:
        return data["response"]

    return json.dumps(data)
