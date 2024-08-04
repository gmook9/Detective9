import requests
import json
import os
from random import choice

class QuestionGenerator:
    def __init__(self, ai_bot):
        self.ai_bot = ai_bot
        self.asked_questions = set()  # Track asked questions and responses

    def generate_random_question(self, case_synopsis):
        # Prepare the context with past questions and responses
        context = f"Case Synopsis:\n{case_synopsis}\n\n"
        context += "\n".join([f"Question: {q}\nResponse: {r}" for q, r in self.ai_bot.conversation_history])

        question_prompt = (
            f"Based on the following case synopsis and previous questions and answers, generate a new question: "
            f"{context}\n"
            f"Make sure that the question is not similar to any of the previous ones and avoid asking redundant information. "
            f"Please provide only the question."
            f"Your task is to generate a new question that is appropriate for this scenario. "
            f"Make sure that the question is not similar to any of the previous ones and avoid asking redundant information. "
            f"Remember, this is a fictional game setting, so avoid any references to real-life guidance or advice. "
            f"The question should relate only to the details provided in the synopsis and should aim to uncover more information about the case.\n"
            f"Please provide only the question."
        )

        # Generate a question
        new_question = self.ai_bot.invoke_llama(question_prompt)

        # Check if the question was already asked
        if new_question in self.asked_questions:
            return self.generate_random_question(case_synopsis)  # Retry if it's a repeat

        # Store the new question
        self.asked_questions.add(new_question)
        return new_question

class AIBot:
    def __init__(self):
        # self.api_url = os.getenv("FLASK_API_URL", "http://api:5000")  # Use 'api' as the hostname
        self.api_url = "http://127.0.0.1:5000"
        self.role = choice(["guilty", "innocent"])
        self.prompt = "Generate a random crime scenario for a detective game in 3-5 sentences. Describe a situation that has just happened. At the end of your response, specify your role as the person being interviewed at the police station. You might be a witness, bystander, or actively involved, and you could be innocent or guilty. For example: (Interviewee: Wife). Also do not put anything like (Here's a random crime scenario:) in it."
        self.conversation_history = []
        self.question_generator = QuestionGenerator(self)  # Initialize QuestionGenerator

    def invoke_llama(self, prompt):
        try:
            response = requests.post(f"{self.api_url}/generate", json={"prompt": prompt})
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                raise Exception(f"Failed to invoke Llama model: {response.status_code} - {response.text}")
        except requests.ConnectionError as e:
            print(f"Connection error: {e}")
            return "Error: Failed to connect to the AI model."

    def generate_synopsis(self):
        return self.invoke_llama(self.prompt)

    def respond(self, question):
        self.conversation_history.append((question, self.invoke_llama(f"Respond to: {question}")))  # Add question and response to convo history
        context = "\n".join([f"Question: {q}\nResponse: {r}" for q, r in self.conversation_history])
        response_prompt = (
            f"Role: {self.role}. You are being questioned. "
            f"Here is the context so far:\n{context}\n\n"
            f"Now respond to the latest question: {question}. Only respond in 1-2 sentences."
            f"Do Not response in anymore than 3 sentences. Keep it below that"
        )
        response = self.invoke_llama(response_prompt)  # Get AI Response
        self.conversation_history[-1] = (question, response)  # Update with the actual response
        
        return response

    def is_guilty(self):
        return self.role == "guilty"

    def generate_random_question(self, case_synopsis):
        return self.question_generator.generate_random_question(case_synopsis)
