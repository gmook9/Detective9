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
        self.conversation_history = []  # Store previous questions and answers

    def generate_synopsis(self):
        return self.llm.invoke(self.prompt)

    def respond(self, question):
        self.conversation_history.append(f"Question: {question}") # Add question to convo history
        context = "\n".join(self.conversation_history)
        response_prompt = (
            f"Role: {self.role}. You are being questioned. "
            f"Here is the context so far:\n{context}\n\n"
            f"Now respond to the latest question: {question}"
        )
        response = self.llm.invoke(response_prompt) # Get AI Response
        self.conversation_history.append(f"Response: {response}") # Add response to convo history
        
        return response

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
