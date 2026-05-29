prices = [100, 250, 75, 400]
lowerprice = [price for price in prices if price > 100]
print(lowerprice)


def greet():
    print("Hello, Harish!")

greet()

def greet(name):              # "name" is an empty slot
    print(f"Hello, {name}!")

greet("Harish")              # "Harish" fills the slot → name = "Harish"
greet("Priya")               # "Priya" fills the slot → name = "Priya"


def describe_model(name, temperature):
    print(f"Model {name} is running at temperature {temperature}")

describe_model("gpt-4", 0.7)
describe_model("claude", 0.2)

def calculate_cost(tokens, price_per_token):
    cost = tokens * price_per_token
    return cost

result = calculate_cost(1000 , .0003)
print(result)


# Version A: uses print
def cost_with_print(tokens, price):
    print(tokens * price)

# Version B: uses return
def cost_with_return(tokens, price):
    return tokens * price

a = cost_with_print(1000, 0.00003)
b = cost_with_return(1000, 0.00003)

print("a holds:", a)
print("b holds:", b)

def calculate_cost_tokens(prompt_tokens, completion_tokens):
    return prompt_tokens + completion_tokens

total = calculate_cost_tokens(150,75)
print(total)

def call_llm(prompt, temperature=0.7):
    print(f"Calling LLM with prompt: '{prompt}' at temperature {temperature}")

call_llm("What is RAG?")
call_llm("Tell me a joke", temperature=1.2)

def estimate_cost(prompts,price_per_token = 0.0003):
    word_count = len(prompts.split())
    estimated_tokens = word_count * 1.3
    cost = estimated_tokens * price_per_token
    return cost

questions =  ["What is retreival augemented generation",
              "Explain vector databases in one paragraph",
              "compare RAG and Fine tuning for domain adamption"] 

for question in questions:
    cost = estimate_cost(question)
    print(f"Question : '{question}'")
    print(f"estimated cost: {cost:.6f}")
    print("-----")