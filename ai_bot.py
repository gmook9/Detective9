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

    def generate_random_question(self):
        question_prompt = (
            "Generate a detective-style question related to a crime investigation, similar to these examples: "
            "\"Where were you on the night of the crime?\", "
            "\"Do you have an alibi?\", "
            "\"Why were you near the crime scene?\""
        )
        return self.llm.invoke(question_prompt)
