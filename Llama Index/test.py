import os 
from langchain_ollama import ChatOllama

model = ChatOllama(
    model = "qwen3:4b"
)

result = model.invoke("What is Paper?")

print(result)