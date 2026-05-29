models = ["gpt-4", "claude", "Mistral"]
for model in models:
    print(f"Testing the model:{model}")
    print(f"completed the model:{model}")
    print("---")
print("This is only once")

for index, model in enumerate(models):
    print (f"Model {index} : {model}")


models = ["gpt-4", "gpt-3.5", "claude", "gemini"]

for model in models:
    if model.startswith("gpt"):
        print(f"{model} is an OpenAI model")
    else:
        print(f"{model} is from a different provider")



config = {"temperature" :"0.7", "max_tokens" : 1000,"model":"gpt-4"}
for key, value in config.items():
    print(f"{key}:{value}")

for number in range(2, 6):
    print(number)


scores = [0.85, 0.42, 0.91, 0.33]
for index, score in enumerate(scores, start =1):
    print(f"Score {index} : {score}")


scores = [0.85, 0.42, 0.91, 0.33]
percentages = []
for score in scores:
    percentages.append(score*100)
print(percentages)

scores = [0.85, 0.42, 0.91, 0.33]
percentages = [score * 100 for score in scores]

models = ["GPT-4", "Claude", "Llama"]
lowercase = [model.lower() for model in models]
print(lowercase)

scores = [0.85, 0.42, 0.91, 0.33]
high_scores = []

for score in scores:
    if score > 0.7:
        high_scores.append(score)

print(high_scores)


scores = [0.85, 0.42, 0.91, 0.33]
high_scores = [score for score in scores if score > 0.7]
print(high_scores)

models = ["gpt-4", "gpt-3.5", "claude", "gemini", "gpt-4o"]
gpt = [model for model in models if model.startswith("gpt")]
print(gpt)
