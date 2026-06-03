import os
from .base import LLMClient
from .mock_client import MockClient
from .openai_client import OpenAIClient
import logging

logger = logging.getLogger(__name__)

def get_llm_client() -> LLMClient:
    provider = os.environ.get("LLM_PROVIDER", "mock").lower()
    
    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not set, falling back to MockClient")
            return MockClient()
        return OpenAIClient()
        
    return MockClient()
