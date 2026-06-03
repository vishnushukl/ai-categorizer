def build_prompt(transaction: dict, company_context: dict) -> str:
    desc = transaction.get("description", "")
    payee = transaction.get("payee", "")
    industry = company_context.get("industry", "")
    coa = company_context.get("chart_of_accounts", [])
    history = company_context.get("historical_transactions", [])
    
    prompt = f"Categorize the following transaction.\n"
    prompt += f"Description: {desc}\n"
    if payee:
        prompt += f"Payee: {payee}\n"
    
    prompt += f"\nCompany Industry: {industry}\n"
    prompt += f"Valid Categories (Chart of Accounts):\n"
    for cat in coa:
        prompt += f"- {cat}\n"
        
    if history:
        prompt += f"\nHistorical Transactions:\n"
        for h in history:
            h_desc = h.get("description", "")
            h_payee = h.get("payee", "")
            h_cat = h.get("category", "")
            prompt += f"- [{h_cat}] {h_desc} (Payee: {h_payee})\n"
            
    return prompt
