from rich.console import Console
from rich.panel import Panel
from rich.text import Text
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
        synopsis = self.ai_bot.generate_synopsis()
        self.console.print(Panel(synopsis, title="Case Synopsis"))
        
        while self.questions_asked < self.max_questions:
            action = self.select_action()
            if action == "Ask a question":
                self.ask_question()
            elif action == "Make a final decision":
                self.make_final_decision()
            elif action == "Exit":
                break
        self.console.print("[bold red]Game over! You've used all your questions.[/bold red]")

    def select_action(self):
        self.console.print("[bold blue]Select an action:[/bold blue]")
        self.console.print("1. Ask a question")
        self.console.print("2. Make a final decision")
        self.console.print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            return "Ask a question"
        elif choice == "2":
            return "Make a final decision"
        elif choice == "3":
            return "Exit"
        else:
            self.console.print("[bold red]Invalid choice. Please try again.[/bold red]")
            return self.select_action()

    def ask_question(self):
        self.console.print("[bold blue]Question Type:[/bold blue]")
        self.console.print("1. Type my own")
        self.console.print("2. Random")
        choice = input("Enter your choice (1/2): ").strip()
        
        if choice == "1":
            user_question = input("Type your question below: ").strip()
        elif choice == "2":
            user_question = get_random_question()
        else:
            self.console.print("[bold red]Invalid choice. Please try again.[/bold red]")
            return self.ask_question()

        self.questions_asked += 1
        self.console.print(Text(f"Question {self.questions_asked}: {user_question}", style="bold red"))
        response = self.ai_bot.respond(user_question)
        self.console.print(Panel(response, title=f"Response [{self.questions_asked}/{self.max_questions}]"))

    def make_final_decision(self):
        self.console.print("[bold blue]Final Decision:[/bold blue]")
        self.console.print("1. Release")
        self.console.print("2. Throw behind bars")
        choice = input("Enter your choice (1/2): ").strip()
        
        if choice == "1":
            decision = "Release"
        elif choice == "2":
            decision = "Throw behind bars"
        else:
            self.console.print("[bold red]Invalid choice. Please try again.[/bold red]")
            return self.make_final_decision()
        
        if self.ai_bot.is_guilty() and decision == "Throw behind bars":
            self.console.print("[bold green]Correct! The suspect was guilty.[/bold green]")
        elif not self.ai_bot.is_guilty() and decision == "Release":
            self.console.print("[bold green]Correct! The suspect was innocent.[/bold green]")
        else:
            self.console.print("[bold red]Wrong decision! You lost.[/bold red]")
        exit()
