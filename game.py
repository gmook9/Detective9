from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from ai_bot import AIBot

class DetectiveGame:
    def __init__(self):
        self.console = Console()
        self.ai_bot = AIBot()
        self.max_questions = 9
        self.questions_asked = 0
        self.exit_game = False  # Flag to track if the game is exited
        self.synopsis = None  # Variable to store the generated synopsis

    def start(self):
        # Welcome message
        self.console.print("[bold green]Welcome, Detective![/bold green]\n")
        self.console.print("[bold yellow]Loading, please wait...[/bold yellow]\n")

        self.synopsis = self.ai_bot.generate_synopsis()  # Store the synopsis
        self.console.print(Panel(self.synopsis, title="Case Synopsis"))
        self.console.print("\n")
        
        while self.questions_asked < self.max_questions and not self.exit_game:
            action = self.select_action()
            if action == "Ask a question":
                self.ask_question()
            elif action == "Make a final decision":
                self.make_final_decision()
            elif action == "Exit":
                self.exit_game = True
                break
        
        if not self.exit_game:
            self.console.print("[bold red]Game over! You've used all your questions.[/bold red]\n")

    def select_action(self):
        self.console.print("[bold blue]Select an action:[/bold blue]")
        self.console.print("1. Ask a question")
        self.console.print("2. Make a final decision")
        self.console.print("3. Exit\n")
        choice = self.console.input("[bold yellow]Enter your choice (1/2/3): [/bold yellow]").strip()
        if choice == "1":
            return "Ask a question"
        elif choice == "2":
            return "Make a final decision"
        elif choice == "3":
            return "Exit"
        else:
            self.console.print("[bold red]Invalid choice. Please try again.[/bold red]\n")
            return self.select_action()

    def ask_question(self):
        self.console.print("\n[bold magenta]Question Type:[/bold magenta]")
        self.console.print("1. Random")
        self.console.print("2. Type my own\n")
        choice = self.console.input("[bold yellow]Enter your choice (1/2): [/bold yellow]").strip()
        
        if choice == "1":
            user_question = self.ai_bot.generate_random_question(self.synopsis)  # Pass the stored synopsis
        elif choice == "2":
            user_question = self.console.input("Type your question below: ").strip()
        else:
            self.console.print("[bold red]Invalid choice. Please try again.[/bold red]\n")
            return self.ask_question()

        self.questions_asked += 1
        self.console.print("\n")
        self.console.print(Text(f"Question {self.questions_asked}: {user_question}", style="bold red"))
        response = self.ai_bot.respond(user_question)
        self.console.print(Panel(response, title=f"Response [{self.questions_asked}/{self.max_questions}]"))
        self.console.print("\n")

    def make_final_decision(self):
        self.console.print("\n[bold bright_magenta]Final Decision:[/bold bright_magenta]")
        self.console.print("1. Release")
        self.console.print("2. Throw behind bars\n")
        choice = self.console.input("[bold yellow]Enter your choice (1/2): [/bold yellow]").strip()
        
        if choice == "1":
            decision = "Release"
        elif choice == "2":
            decision = "Throw behind bars"
        else:
            self.console.print("[bold red]Invalid choice. Please try again.[/bold red]\n")
            return self.make_final_decision()
        
        self.console.print("\n")
        if self.ai_bot.is_guilty() and decision == "Throw behind bars":
            self.console.print("[bold green]Correct! The suspect was guilty.[/bold green]\n")
        elif not self.ai_bot.is_guilty() and decision == "Release":
            self.console.print("[bold green]Correct! The suspect was innocent.[/bold green]\n")
        else:
            self.console.print("[bold red]Wrong decision! You lost.[/bold red]\n")
        exit()
