import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables once when the script starts
load_dotenv()

# Create the client once, reuse it across calls
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_llm(prompt, system_message="You are a helpful AI assistant.", model="llama-3.3-70b-versatile"):
    """
    Send a prompt to the LLM and return its reply.
    
    Args:
        prompt: The user's question or instruction.
        system_message: Background instructions for the model (default: generic helpful).
        model: Which model to use (default: llama-3.3-70b-versatile).
    
    Returns:
        The model's text reply as a string.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# --- Test the function ---
if __name__ == "__main__":
    # Basic call with defaults
    answer1 = ask_llm("What is RAG in one sentence?")
    print("Q1 answer:")
    print(answer1)
    print()

    # Same question with a domain-specific system message
    answer2 = ask_llm(
        prompt="What is RAG in one sentence?",
        system_message="You are an AI engineering expert. Answer in the context of AI/ML only."
    )
    print("Q2 answer (with system message):")
    print(answer2)
    print()

    # A completely different question, reusing the same function
    answer3 = ask_llm("Name three vector databases.")
    print("Q3 answer:")
    print(answer3)