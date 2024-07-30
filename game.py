from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from ai_bot import AIBot
from questions import get_random_question

class DetectiveGame:
    def __init__(self):
        self.console = Console()
        self.ai_bot = AIBot()
        self.max_questions = 9
        self.questions_asked = 0

    def start(self):
        self.console.print("[bold green]Welcome, Detective![/bold green]")
        while self.questions_asked < self.max_questions:
            action = Prompt.ask("Select an action", choices=["Ask a question", "Make a final decision", "Exit"])
            if action == "Ask a question":
                self.ask_question()
            elif action == "Make a final decision":
                self.make_final_decision()
            elif action == "Exit":
                break
        self.console.print("[bold red]Game over! You've used all your questions.[/bold red]")

    def ask_question(self):
        question = Prompt.ask("Do you want to type your own question or get a random one?", choices=["Type my own", "Random"])
        if question == "Type my own":
            user_question = Prompt.ask("Type your question below")
        else:
            user_question = get_random_question()

        response = self.ai_bot.respond(user_question)
        self.questions_asked += 1
        self.console.print(Panel(response, title=f"Response [{self.questions_asked}/{self.max_questions}]"))

    def make_final_decision(self):
        decision = Prompt.ask("What is your final decision?", choices=["Release", "Throw behind bars"])
        if self.ai_bot.is_guilty() and decision == "Throw behind bars":
            self.console.print("[bold green]Correct! The suspect was guilty.[/bold green]")
        elif not self.ai_bot.is_guilty() and decision == "Release":
            self.console.print("[bold green]Correct! The suspect was innocent.[/bold green]")
        else:
            self.console.print("[bold red]Wrong decision! You lost.[/bold red]")
        exit()

