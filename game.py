import os
import time
import requests
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

    def wait_for_api(self, timeout=30):
        """Wait for the API to be available before starting the game."""
        self.console.print("[bold yellow]Waiting for the API to be available...[/bold yellow]")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.ai_bot.api_url}/health")
                if response.status_code == 200:
                    self.console.print("[bold green]API is available! Starting the game...[/bold green]")
                    return
            except requests.ConnectionError:
                print(".", end="", flush=True)  # Use the built-in print function
                time.sleep(1)
        self.console.print("[bold red]\nAPI is not available. Exiting.[/bold red]")
        exit(1)

    def start(self):
        # Wait for the API to be ready
        self.wait_for_api()

        # Welcome message
        self.console.print("[bold green]Welcome, Detective![/bold green]\n")
        self.console.print("[bold yellow]Loading, please wait...[/bold yellow]\n")

        self.synopsis = self.ai_bot.generate_synopsis()  # Store the synopsis
        if not self.synopsis:
            self.console.print("[bold red]Error: Failed to generate a case synopsis.[/bold red]")
            return

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

        try:
            # Make the API call to get the user's action
            response = requests.post(f"{self.ai_bot.api_url}/select_action", json={"choice": "1"})  # Example: default to "1" for testing
            response.raise_for_status()
            
            action_choice = response.json().get("action")
            if not action_choice:
                raise ValueError("Invalid response from the API")
            
            return action_choice

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 400:
                self.console.print(f"[bold red]Invalid choice. Please try again.[/bold red]\n")
                return "Exit"  # Exit the loop or handle it based on your game logic
            else:
                self.console.print(f"[bold red]Error: HTTP error occurred - {str(http_err)}[/bold red]\n")
                return "Exit"
        except requests.exceptions.RequestException as e:
            self.console.print(f"[bold red]Error: Failed to communicate with the API - {str(e)}[/bold red]\n")
            return "Exit"
        except ValueError as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]\n")
            return "Exit"

    def ask_question(self):
        self.console.print("\n[bold magenta]Question Type:[/bold magenta]")
        self.console.print("1. Random")
        self.console.print("2. Type my own\n")

        try:
            # Get user choice for question type
            choice = self.console.input("[bold yellow]Enter your choice (1/2): [/bold yellow]").strip()

            if choice == "1":
                # Send request to API to generate a random question based on the case synopsis
                response = requests.post(
                    f"{self.ai_bot.api_url}/select_question_type",
                    json={"type": "random", "case_synopsis": self.synopsis}
                )
            elif choice == "2":
                # Get user input for a manual question
                user_question = self.console.input("[bold yellow]Enter your question: [/bold yellow]").strip()
                response = requests.post(
                    f"{self.ai_bot.api_url}/select_question_type",
                    json={"type": "manual", "question": user_question}
                )
            else:
                self.console.print("[bold red]Invalid choice. Please try again.[/bold red]\n")
                return self.ask_question()

            # Handle the API response
            if response.status_code == 400:
                self.console.print("[bold red]Invalid choice or input. Please try again.[/bold red]\n")
                return

            response.raise_for_status()
            user_question = response.json().get("question")

            self.process_question(user_question)

        except requests.exceptions.RequestException as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]\n")
            return



    def process_question(self, user_question):
        context = f"Case Synopsis:\n{self.synopsis}\n\n"
        context += "\n".join([f"Question: {q}\nResponse: {r}" for q, r in self.ai_bot.conversation_history])
        context += f"\n\nNew Question: {user_question}\n\nPlease respond in 1-2 sentences."

        response = self.ai_bot.invoke_llama(context)  # Use the correct method to get AI Response
        if not response:
            self.console.print("[bold red]Error: Failed to generate a response from the AI model.[/bold red]")
            return

        self.ai_bot.conversation_history.append((user_question, response))  # Add the user question and AI response to convo history

        self.questions_asked += 1
        self.console.print("\n")
        self.console.print(Text(f"Question {self.questions_asked}: {user_question}", style="bold red"))
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
        self.exit_game = True
