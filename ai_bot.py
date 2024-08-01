from random import choice
from langchain_community.llms import Ollama

# TO-DO FIX THIS
class QuestionGenerator:
    def __init__(self, ai_bot):
        self.ai_bot = ai_bot

    def generate_random_question(self):
        case_synopsis = self.ai_bot.generate_synopsis()

        # Define a constrained prompt for generating a relevant question
        question_prompt = (
            f"You are a detective. Below is a case synopsis:\n\n"
            f"'{case_synopsis}'\n\n"
            f"Your task is to generate one specific question related only to the details mentioned in the case synopsis above. "
            f"The question must directly reference people, events, locations, or objects mentioned. "
            f"Do not introduce any new characters, locations, or events. "
            f"Only ask about what is described in the synopsis.\n"
            f"Please provide only the question."
        )
        return self.ai_bot.llm.invoke(question_prompt)

class AIBot:
    def __init__(self):
        self.llm = Ollama(model="llama3")
        self.role = choice(["guilty", "innocent"])
        self.prompt = "Generate a random crime scenario for a detective game in 3-5 sentences. Describe a situation that has just happened. At the end of your response, specify your role as the person being interviewed at the police station. You might be a witness, bystander, or actively involved, and you could be innocent or guilty. For example: (Interviewee: Wife). Also do not put anything like (Here's a random crime scenario:) in it."
        self.conversation_history = []  # Store previous questions and answers
        self.question_generator = QuestionGenerator(self)  # Initialize the QuestionGenerator with AIBot

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
        return self.question_generator.generate_random_question()
