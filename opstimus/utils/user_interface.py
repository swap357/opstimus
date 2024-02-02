from rich import print
from rich.prompt import Confirm
from rich.markdown import Markdown
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner

class UserInterface:

    def __init__(self) -> None:
        self.console = Console()

    def get_user_confirmation(self, message):
        confirmation = Confirm.ask(message)
        return confirmation
    
    def print_yaml(self,content):
        self.console.print(Markdown(f"```yaml\n{content}\n```"))

    def print_python(self,content):
        self.console.print(Markdown(f"```python\n{content}\n```"))
    
    def print_markdown(self,content):
        self.console.print(Markdown(f"\n{content}\n"))

    def print(self,content):
        self.console.print(f"{content}")

    def print_panel(self,content):
        self.console.print(Panel(f"{content}"))
    
    def status(self,text):
        self.console.status(text)