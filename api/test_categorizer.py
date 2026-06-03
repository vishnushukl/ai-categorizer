from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import json
import os
from unittest.mock import patch
from api.llm.mock_client import MockClient

class CategorizerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        os.environ["LLM_PROVIDER"] = "mock"
        
        self.valid_payload = {
            "transaction": {
                "description": "AWS Cloud Services",
                "payee": "Amazon"
            },
            "company_context": {
                "company_id": "acme-123",
                "industry": "Software",
                "chart_of_accounts": [
                    "Software Subscriptions",
                    "Office Supplies",
                    "Travel"
                ],
                "historical_transactions": []
            }
        }
        
    def test_health_check(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_categorize_success(self):
        response = self.client.post("/api/categorize/", data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["category"], "Software Subscriptions")
        self.assertTrue(data["is_valid_category"])

    def test_categorize_invalid_request_missing_company_context(self):
        invalid_payload = {"transaction": {"description": "AWS"}}
        response = self.client.post("/api/categorize/", data=invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_categorize_no_payee(self):
        # Edge case: No payee should still work
        payload = self.valid_payload.copy()
        payload["transaction"] = {"description": "AWS"}
        response = self.client.post("/api/categorize/", data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("api.services.categorizer.get_llm_client")
    def test_llm_returns_invalid_category(self, mock_get_client):
        # Edge case: LLM hallucinates a category not in CoA
        mock_response = json.dumps({"category": "Space Ships", "confidence": 0.9, "reasoning": "..."})
        mock_get_client.return_value = MockClient(override_response=mock_response)
        
        response = self.client.post("/api/categorize/", data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["category"], "Uncategorized")
        self.assertFalse(data["is_valid_category"])
        self.assertEqual(data["suggested_category_raw"], "Space Ships")
        self.assertLessEqual(data["confidence"], 0.3) # Confidence capped

    @patch("api.services.categorizer.get_llm_client")
    def test_llm_returns_malformed_json(self, mock_get_client):
        # Edge case: LLM returns completely broken JSON
        mock_get_client.return_value = MockClient(override_response="This is not json.")
        
        response = self.client.post("/api/categorize/", data=self.valid_payload, format="json")
        # The parser catches this and returns Uncategorized
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["category"], "Uncategorized")
        self.assertEqual(data["confidence"], 0.0)

    @patch("api.services.categorizer.get_llm_client")
    def test_llm_exception_unavailable(self, mock_get_client):
        # Edge case: LLM completely crashes or network fails
        client_instance = MockClient()
        def crash(*args, **kwargs):
            raise Exception("API down")
        client_instance.generate_categorization = crash
        mock_get_client.return_value = client_instance
        
        response = self.client.post("/api/categorize/", data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

    @patch("api.services.categorizer.get_llm_client")
    def test_confidence_heuristic_boost(self, mock_get_client):
        # Edge case: Payee matches history, confidence should be boosted
        mock_response = json.dumps({"category": "Travel", "confidence": 0.5, "reasoning": "..."})
        mock_get_client.return_value = MockClient(override_response=mock_response)
        
        payload = self.valid_payload.copy()
        payload["transaction"] = {"description": "Uber Ride", "payee": "Uber"}
        payload["company_context"]["historical_transactions"] = [
            {"description": "Previous Uber", "payee": "Uber", "category": "Travel"}
        ]
        
        response = self.client.post("/api/categorize/", data=payload, format="json")
        data = response.json()
        self.assertEqual(data["category"], "Travel")
        self.assertEqual(data["confidence"], 0.6) # 0.5 + 0.1
        self.assertIn("boosted due to historical payee", data["reasoning"])
