import json
import logging

logger = logging.getLogger(__name__)

def parse_and_validate(llm_response: str, chart_of_accounts: list[str]) -> dict:
    try:
        parsed = json.loads(llm_response)
    except json.JSONDecodeError:
        logger.error("Failed to parse LLM output as JSON")
        return {
            "category": "Uncategorized",
            "confidence": 0.0,
            "reasoning": "Failed to parse LLM response.",
            "is_valid_category": False,
            "suggested_category_raw": llm_response
        }
        
    category = parsed.get("category", "Uncategorized")
    # Clean confidence value
    try:
        confidence = float(parsed.get("confidence", 0.0))
    except (ValueError, TypeError):
        confidence = 0.0
        
    reasoning = parsed.get("reasoning", "")
    
    is_valid = category in chart_of_accounts
    suggested_raw = None
    
    if not is_valid:
        suggested_raw = category
        category = "Uncategorized"
        confidence = min(confidence, 0.3)
        
    return {
        "category": category,
        "confidence": confidence,
        "reasoning": reasoning,
        "is_valid_category": is_valid,
        "suggested_category_raw": suggested_raw
    }
