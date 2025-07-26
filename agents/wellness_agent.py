# agents/wellness_agent.py

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from instruction import GENETIC_WELLNESS_AGENT_INSTRUCTION

class GeneticWellnessAgent(Agent):
    """
    An ADK Agent designed to answer general genetic wellness and scientific questions
    by leveraging a foundational LLM's knowledge.
    """
    def __init__(self, name: str, instruction: str, model: LiteLlm):
        super().__init__(name=name, instruction=instruction, model=model)
