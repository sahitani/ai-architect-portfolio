from day8_first_llm import ask_llm


def extract_json(text):
    """Extract JSON from LLM output, handling common malformations."""
    # Strip whitespace
    text = text.strip()
    
    # If wrapped in markdown code fences, remove them
    if text.startswith("```"):
        # Remove opening fence (could be ```json or just ```)
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        # Remove closing fence
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    
    return json.loads(text)

def classify_message(message_text):
    """Classify a customer support message into structured fields.
    
    Args:
        message_text: The raw customer message string.
    
    Returns:
        A dict with keys: urgency, category, is_complaint, needs_human.
        Returns None if the LLM output couldn't be parsed.
    """
    system_msg = """You are a customer support message classifier.

For each customer message, return a JSON object with EXACTLY these four keys:
- "urgency": one of "low", "medium", "high"
- "category": one of "billing", "account_access", "feature_request", "bug_report", "other"
- "is_complaint": true or false
- "needs_human": true or false (true if a human agent should review)

Rules:
- Respond with ONLY the JSON object, nothing else
- No markdown code fences, no explanations, no preamble
- All keys must be present in every response
- Use lowercase for string values"""
    
    raw_response = ask_llm(prompt=message_text, system_message=system_msg)
    
    try:
        return extract_json(raw_response)
    except json.JSONDecodeError as e:
        print(f"  ⚠ Failed to parse LLM response: {e}")
        print(f"    Raw response: {raw_response[:80]}...")
        return None

messages = [
    "My account is locked and I can't access my data. Need this fixed NOW.",
    "Wondering if you'll be adding dark mode anytime soon.",
    "Got charged twice for the same subscription this month.",
]

# Naive approach — no system message, no format constraints
for msg in messages:
    response = ask_llm(f"What is the urgency level of this customer message: '{msg}'?")
    print(f"Message: {msg[:60]}...")
    print(f"Response: {response}")
    print("---")

    # --- Structured approach ---

print("\n\n=== STRUCTURED OUTPUT ATTEMPT ===\n")

system_msg = """You are a customer support urgency classifier.
You classify customer messages into exactly one of three urgency levels: low, medium, or high.

Rules:
- Respond with ONLY the single word: low, medium, or high
- All lowercase
- No punctuation, no explanation, no additional text
- If unsure, choose medium"""

for msg in messages:
    response = ask_llm(prompt=msg, system_message=system_msg)
    print(f"Message: {msg[:60]}...")
    print(f"Urgency: {response}")
    print("---")

import json

print("\n\n=== STRUCTURED JSON OUTPUT ===\n")

json_system_msg = """You are a customer support message classifier.

For each customer message, return a JSON object with EXACTLY these four keys:
- "urgency": one of "low", "medium", "high"
- "category": one of "billing", "account_access", "feature_request", "bug_report", "other"
- "is_complaint": true or false
- "needs_human": true or false (true if a human agent should review; false if automated systems can handle)

Rules:
- Respond with ONLY the JSON object, nothing else
- No markdown code fences, no explanations, no preamble
- All keys must be present in every response
- Use lowercase for string values"""

for msg in messages:
    raw_response = ask_llm(prompt=msg, system_message=json_system_msg)
    
    # Convert the JSON text into a Python dict
    parsed = extract_json(raw_response)
    
    print(f"Message: {msg[:60]}...")
    print(f"Parsed dict: {parsed}")
    print(f"  Urgency:     {parsed['urgency']}")
    print(f"  Category:    {parsed['category']}")
    print(f"  Complaint?   {parsed['is_complaint']}")
    print(f"  Needs human? {parsed['needs_human']}")
    print("---")


print("\n\n=== WHAT HAPPENS WHEN LLM MISBEHAVES ===\n")

# Simulate a misbehaved LLM response
bad_response = '''Sure! Here's the JSON you asked for:
```json
{"urgency": "high", "category": "billing", "is_complaint": true, "needs_human": true}
```
Let me know if you need anything else!'''

try:
    parsed = extract_json(bad_response)
    print(f"Parsed: {parsed}")
except json.JSONDecodeError as e:
    print(f"JSON parsing FAILED: {e}")
    print(f"Raw response was: {bad_response[:80]}...")


print("\n\n=== USING THE CAPSTONE FUNCTION ===\n")

new_messages = [
    "The login page is throwing a 500 error every time I try to sign in.",
    "Hey! Could you add support for German language in the next release?",
    "I've been waiting THREE WEEKS for a refund. This is unacceptable.",
]

for msg in new_messages:
    result = classify_message(msg)
    if result:
        print(f"Message: {msg[:60]}...")
        print(f"  → {result}")
        print("---")
    else:
        print(f"Message: {msg[:60]}...")
        print(f"  → CLASSIFICATION FAILED")
        print("---")