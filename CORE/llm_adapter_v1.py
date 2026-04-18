
import requests


class LocalLLMAdapter:
    def __init__(self, model="llama3", host="http://localhost:11434"):
        self.model = model
        self.host = host

    def generate(self, prompt: str):
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            if response.status_code == 200:
                return response.json().get("response", "").strip()

            return f"[LLM ERROR] {response.status_code}"

        except Exception as e:
            return f"[LLM EXCEPTION] {str(e)}"
