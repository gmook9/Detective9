from random import choice
from langchain_community.llms import Ollama

class AIBot:
    def __init__(self):
        self.llm = Ollama(model="llama3")
        self.role = choice(["guilty", "innocent"])

    def respond(self, question):
        # Simulating a response from the AI
        return self.llm.invoke(f"Role: {self.role}. Question: {question}")

    def is_guilty(self):
        return self.role == "guilty"
