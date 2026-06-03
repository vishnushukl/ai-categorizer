import logging
from ..llm.factory import get_llm_client
from .prompt_engine import build_prompt
from .output_parser import parse_and_validate
from .confidence_scorer import adjust_confidence

logger = logging.getLogger(__name__)

def process_transaction(transaction: dict, company_context: dict) -> dict:
    logger.info(f"categorize: company={company_context.get('company_id')} industry={company_context.get('industry')}")
    
    llm_client = get_llm_client()
    prompt = build_prompt(transaction, company_context)
    
    schema = {
        "type": "object",
        "properties": {
            "category": {"type": "string"},
            "confidence": {"type": "number"},
            "reasoning": {"type": "string"}
        },
        "required": ["category", "confidence", "reasoning"]
    }
    
    try:
        llm_response = llm_client.generate_categorization(prompt, schema)
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        raise ValueError("llm_unavailable")
        
    parsed = parse_and_validate(llm_response, company_context.get("chart_of_accounts", []))
    final_result = adjust_confidence(parsed, transaction, company_context.get("historical_transactions", []))
    
    final_result["model"] = getattr(llm_client, "model", "mock")
    
    return final_result
