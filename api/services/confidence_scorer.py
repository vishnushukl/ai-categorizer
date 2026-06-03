def adjust_confidence(parsed_result: dict, transaction: dict, history: list[dict]) -> dict:
    # If invalid category, confidence is already capped in parser
    if not parsed_result.get("is_valid_category", False):
        return parsed_result
        
    # Heuristic: boost confidence if payee exactly matches a historical transaction with same category
    payee = transaction.get("payee")
    category = parsed_result.get("category")
    
    if payee and payee.strip():
        for h in history:
            h_payee = h.get("payee")
            if h_payee and h_payee.lower().strip() == payee.lower().strip():
                if h.get("category") == category:
                    parsed_result["confidence"] = min(1.0, parsed_result["confidence"] + 0.1)
                    parsed_result["reasoning"] += " (Confidence boosted due to historical payee match.)"
                    break
                    
    return parsed_result
