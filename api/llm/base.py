from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMClient(ABC):
    @abstractmethod
    def generate_categorization(self, prompt: str, schema: Dict[str, Any]) -> str:
        """
        Generate a categorization based on the prompt.
        Must return a JSON string matching the schema.
        """
        pass
