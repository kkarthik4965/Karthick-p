from google import genai
from google.genai import types

import config


class GeminiDocumentGenerator:
    """Builds a structured prompt and sends it to Gemini."""

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or config.GEMINI_MODEL
        self._client = None

    def _get_client(self):
        if self._client is None:
            if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "your_api_key_here":
                raise RuntimeError("GEMINI_API_KEY is missing. Add it to the .env file.")
            self._client = genai.Client(api_key=config.GEMINI_API_KEY)
        return self._client

    def build_prompt(self, document_type, parties, terms, dates) -> str:
        return (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions (semicolon separated): {terms}\n"
            "Ensure formal legal structure with multiple sections and legal clauses.\n"
            "Formatting rules: output plain text only, no markdown symbols (no #, *, or backticks). "
            "Put the document title on the first line. Number each section heading on its own line "
            "like '1. Services:'. Use '- ' for bullet points. Use [square brackets] for details "
            "that were not provided. End with a signature block for every party."
        )

    def generate_document(self, document_type, parties, terms, dates) -> str:
        prompt = self.build_prompt(document_type, parties, terms, dates)
        response = self._get_client().models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.4),
        )
        if not response.text:
            raise RuntimeError("Gemini returned an empty response. Try again.")
        return response.text
