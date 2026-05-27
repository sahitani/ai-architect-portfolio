# day 3 python basics

# variables and Data types
model_name = "GPT - 4.0"
temprature = 0.7
max_tokens = 1000
streaming = True
api_key = None

#Print each variables with it types
print(model_name),type(model_name)
print(temprature),type(temprature)
print(max_tokens, type(max_tokens))
print(streaming,type(streaming))
print(api_key,type(api_key))

#------Topic 2: Strings-------

#Basic f-string
username = "Harish"
greeting = f"Hello,{username}! ready for day 3?"
print(greeting)

#Expression under f-string
tokens = 1500
cost_per_token = 0.0003
print(f"cost: ${cost_per_token*tokens:.4f}")

# Multi line Prompt
context = "Python is a dynamically typed, interpreted programming language."
question = "What kind of language is Python?"

prompt = f"""You are a helpful assistant. Answer using the context.

Context:
{context}

Question:
{question}

Answer:"""

print(prompt)
# String cleanup methods
messy_input = "What is RAG?\n"
clean_input = messy_input.strip().lower()
print(f"Cleaned: '{clean_input}'")
