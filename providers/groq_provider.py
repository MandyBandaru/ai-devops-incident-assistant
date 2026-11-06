
import os
from groq import Groq

from providers.base import AIProvider
from prompt_builder import build_troubleshooting_prompt


class GroqProvider(AIProvider): #Because GroqProvider inherits from AIProvider #AIProvider is Parent class — defines the plan &&& &&& GroqProvider is Child class — implements the plan

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured")

        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-20b"

    def analyze_incident(self, incident: str) -> dict: # ABSTRACT METHOD IMPLEMENTATION — because analyze_incident is defined in base.py
        prompt = build_troubleshooting_prompt(incident) 

        instructions = (
            "You are an experienced DevOps engineer. "
            "Explain incidents in simple English. "
            "Never claim a root cause is confirmed without evidence. "
            "Give practical diagnostic commands.\n\n"
            + prompt
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": instructions}
            ],
            temperature=0.6,
            max_completion_tokens=1000
        )

                # Validate AI response
                #  #For our incident assistant, we require:
                #- A response must contain at least one choice.
                #- The response must contain text.
                #- The text must not be empty.
        if not response.choices:
            raise ValueError("Groq returned no response choices")

        analysis = response.choices[0].message.content

        if not analysis or not analysis.strip():
            raise ValueError("Groq returned an empty AI response")

        return {
            "provider": "groq",
            "model": self.model,
            "incident": incident,
            "analysis": analysis,
            "root_cause_confirmed": False
        }



 