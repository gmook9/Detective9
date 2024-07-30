import json
import random

def load_questions(filename="questions.json"):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data["questions"]

questions = load_questions()

def get_random_question():
    return random.choice(questions)
