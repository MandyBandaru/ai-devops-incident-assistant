from providers.base import AIProvider
from ai_client_simulation import get_ai_response


class MockProvider(AIProvider):

    def analyze_incident(self, incident: str) -> dict: #pulling/syntax for abstract method from base.py

        return get_ai_response(incident)