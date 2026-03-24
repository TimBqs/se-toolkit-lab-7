"""Intent router - uses LLM to understand plain text queries."""

from services.llm_client import llm_client
from services.tools import SYSTEM_PROMPT, TOOLS


def route_intent(user_message: str) -> str:
    """
    Route a plain text message to the LLM for intent resolution.
    
    Args:
        user_message: The user's input text
        
    Returns:
        Response text from the LLM
    """
    return llm_client.chat_with_tools(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message,
        tools=TOOLS,
        max_iterations=5,
    )
