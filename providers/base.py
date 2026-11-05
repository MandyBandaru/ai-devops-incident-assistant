from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def analyze_incident(self, incident: str) -> dict:
        pass