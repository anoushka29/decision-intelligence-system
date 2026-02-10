import ollama

print("Testing Ollama...")

response = ollama.chat(
    model='llama3.2',
    messages=[
        {'role': 'user', 'content': 'Explain Monte Carlo simulation in one sentence'}
    ]
)

print("✅ Ollama is working!")
print("Response:", response['message']['content'])
