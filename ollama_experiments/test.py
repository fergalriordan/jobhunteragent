import ollama

with open('prompt.txt', 'r') as file:
    prompt = file.read()

# Use the generate function for a one-off prompt
result = ollama.generate(model='deepseek-r1:1.5b', prompt=prompt)
print(result['response'])