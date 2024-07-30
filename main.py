from langchain_community.llms import Ollama
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

llm = Ollama(model="llama3")

question = Prompt.ask(f"[bold blue]{llm.model}[/bold blue]. Please type question below")

response = llm.invoke(question)

console.print(Panel(response, title="Response"))
