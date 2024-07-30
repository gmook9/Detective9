import os
from random import choice
from langchain_community.llms import Ollama
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AIBot:
    def __init__(self):
        self.llm = Ollama(model="llama3")
        self.role = choice(["guilty", "innocent"])
        self.prompt = os.getenv("PROMPT")

    def generate_synopsis(self):
        return self.llm.invoke(self.prompt)

    def respond(self, question):
        return self.llm.invoke(f"Role: {self.role}. Question: {question}")

    def is_guilty(self):
        return self.role == "guilty"
