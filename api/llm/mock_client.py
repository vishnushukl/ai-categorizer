from .base import LLMClient
import json
from typing import Dict, Any

class MockClient(LLMClient):
    def __init__(self, override_response: str = None):
        self.override_response = override_response

    def generate_categorization(self, prompt: str, schema: Dict[str, Any]) -> str:
        if self.override_response:
            return self.override_response
        return json.dumps({
            "category": "Software Subscriptions",
            "confidence": 0.8,
            "reasoning": "Mock reasoning"
        })
