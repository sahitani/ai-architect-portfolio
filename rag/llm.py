"""LLM utilities for interacting with hosted models via Groq."""

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables and create the client once
load_dotenv()
_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_llm(prompt, system_message="You are a helpful AI assistant.", model="llama-3.3-70b-versatile"):
    """Send a prompt to the LLM and return its reply.
    
    Args:
        prompt: The user's question or instruction.
        system_message: Background instructions for the model (default: generic).
        model: Which model to use.
    
    Returns:
        The model's text reply as a string.
    """
    response = _client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content