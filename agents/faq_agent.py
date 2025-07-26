# agents/faq_agent.py

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

class CustomerSupportAgent(Agent):
    """
    An ADK Agent designed to answer NuGenomics-specific customer support questions
    based on a provided FAQ knowledge base.
    """
    def __init__(self, name: str, instruction: str, faqs: dict, model: LiteLlm):
        """
        Initializes the CustomerSupportAgent.

        Args:
            name (str): The name of the agent.
            instruction (str): The base instruction string for the agent.
            faqs (dict): A dictionary containing question-answer pairs for the FAQs.
            model (LiteLlm): The language model instance for the agent.
        """
        # Append the FAQ knowledge base to the instruction
        faq_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in faqs.items()])
        full_instruction = f"{instruction}\n\nFAQ Knowledge Base:\n{faq_text}\n\nBased on the above, answer the user's query. If the answer is not in the FAQ, state that you don't have specific information but can offer general advice."
        
        # Call the parent constructor with the new, combined instruction
        super().__init__(name=name, instruction=full_instruction, model=model)
        
        # Store faqs in object.__setattr__ to bypass potential Pydantic validation in the parent class
        object.__setattr__(self, 'faqs', faqs)
