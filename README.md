# AI Categorizer Service

A backend-only AI-powered transaction categorization service built with Django REST Framework.
This project is an engineering implementation exercise providing a clean API design and a deterministic structured JSON output via an LLM integration layer.

## Architecture
- **Framework:** Django & Django REST Framework
- **LLM Abstraction:** Model-agnostic design (includes Mock and OpenAI-compatible wrappers).
- **Service Layer:** Clean separation between `prompt_engine`, `output_parser`, and `confidence_scorer`.

## Requirements
- Python 3.10+
- `pip install -r requirements.txt` (or install via the instructions below)

## Setup & Running Locally

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install django djangorestframework openai pydantic
   ```
3. Configure the API Key:
   Export the variables in your terminal:
   ```bash
   export LLM_PROVIDER=openai
   export OPENAI_API_KEY=your_sk_key_here
   export OPENAI_MODEL=gpt-4o-mini
   ```
   *Note: If no API key is provided, the service safely falls back to a Mock client for testing.*

4. Run the server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### 1. Health Check
`GET /api/health/`

### 2. Categorize Transaction
`POST /api/categorize/`

**Request Schema:**
```json
{
  "transaction": {
    "description": "Figma Pro",
    "payee": "Figma"
  },
  "company_context": {
    "company_id": "acme-123",
    "industry": "Software",
    "chart_of_accounts": ["Software Subscriptions", "Office Supplies", "Travel"],
    "historical_transactions": [
      {"description": "AWS", "payee": "Amazon", "category": "Software Subscriptions"}
    ]
  }
}
```

**Response Schema:**
```json
{
  "category": "Software Subscriptions",
  "confidence": 0.95,
  "reasoning": "Figma is a SaaS design tool, matching the Software Subscriptions category.",
  "is_valid_category": true,
  "suggested_category_raw": null,
  "model": "gpt-4o-mini"
}
```

## Evaluation & Testing
Run the evaluation script to test Top-1 category match and confidence sampling on sample transactions:
```bash
python evaluate.py
```

Run the unit test suite:
```bash
python manage.py test api
```
