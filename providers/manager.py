import os

from providers.mock_provider import MockProvider

# Future providers — not implemented yet
# from providers.bedrock_provider import BedrockProvider
from providers.groq_provider import GroqProvider
# from providers.ollama_provider import OllamaProvider


def get_provider():

    provider_name = os.getenv("AI_PROVIDER", "mock").lower()

    # Currently available provider
    if provider_name == "mock":
        return MockProvider()

    # Future provider selections
    # if provider_name == "bedrock":
    #     return BedrockProvider()

    if provider_name == "groq":
        return GroqProvider()

    # if provider_name == "ollama":
    #     return OllamaProvider()

    raise ValueError(f"Unsupported AI provider: {provider_name}")