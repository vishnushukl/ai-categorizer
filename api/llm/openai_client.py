import json
import os
from openai import OpenAI
from .base import LLMClient
from typing import Dict, Any

class OpenAIClient(LLMClient):
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "mock-key"))
        self.model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    def generate_categorization(self, prompt: str, schema: Dict[str, Any]) -> str:
        # Pass schema into the prompt to guide output, ensuring json_object format is valid.
        schema_prompt = prompt + f"\n\nPlease output JSON exactly matching this schema:\n{json.dumps(schema, indent=2)}"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a financial categorization assistant. Return strict JSON matching the user's requested schema. Do not include markdown formatting or comments."},
                {"role": "user", "content": schema_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        return response.choices[0].message.content
