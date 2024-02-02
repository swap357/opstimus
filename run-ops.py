# Import necessary libraries
from rich.console import Console
from rich.table import Table
# from colorama import Fore, Style
import yaml
from opstimus.utils.user_interface import UserInterface
from opstimus.ansible.config_manager import AnsibleManager
from opstimus.utils.file_storage import FileStorage
from opstimus.ansible.execution_engine import AnsibleExecutionEngine
from opstimus.cli import CLI

# Main function to run the CLI tool
class Ops:
    TASKS_DIR = "tasks"

    def __init__(self):
        self.console = Console()
        self.cli = CLI()
        self.args = self.cli.parse_args()

        self.file_storage = FileStorage(self.TASKS_DIR)
        self.ansible_mgr = AnsibleManager(self.file_storage)
        self.execution_engine = AnsibleExecutionEngine(self.TASKS_DIR)
        
        self.ui = UserInterface()

        self.command_mapping = {
                'new': self.create_task,
                'run': self.run_task,
                'ls': self.list_tasks,
                'rm': self.delete_task,
                'update': self.update_task,
                'cat': self.view_task,
                'help': self.cli.parser.print_help,
            }
    
    def execute_command(self):
        command = self.args.command
        command_function = self.command_mapping.get(command)
        if command_function:
            command_function()
        else:
            self.ui.print("[red]Invalid command.[/red]")
            self.cli.parser.print_help()

    def list_tasks(self):
        tasks = self.ansible_mgr.list_configs()
        if not tasks:
            self.ui.print_panel(f"No tasks found.")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Task", style="dim", width=20)
        for task in tasks:
            table.add_row(task)
        self.console.print(table)

    def view_task(self,task=''):
        task = self.args.task
        playbook_content = self.ansible_mgr.get_config(task)
        if playbook_content:
            self.ui.print_yaml(playbook_content)
        else:
            self.ui.print_panel(f"[red]No config exists for task: {task}[/red]")
    
    # todo
    def create_task(self,user_query=None):
        if not user_query:
            user_query = self.args.query

        playbook = self.file_storage.get_file_content(user_query)

        if playbook is None:
            playbook_name, playbook_description, playbook_content = self.ansible_mgr.create_config(user_query)
            if playbook_name and playbook_description and playbook_content:
                self.ui.print_yaml(yaml.safe_dump([playbook_content], default_flow_style=False, sort_keys=False, explicit_start=True, indent=2, width=80))
                self.ui.print_panel(f"CREATED:\nName: {playbook_name}\nDescription: {playbook_description}")
                self.ansible_mgr.save_config(playbook_name, playbook_description, playbook_content)
            else:
                self.ui.print_panel(f"[red]Error creating task config![/red]")
        else:
            self.ui.print(f"[green]Task config {user_query} already exists.[/green]")

    # todo
    def run_task(self):
        task = self.args.task
        self.ui.print("")
        pb = self.ansible_mgr.get_config(task)
        if not pb:
            self.ui.print_panel(f"[red]No config exists for task: {task}[/red]")
            confirmation_msg = f"Would you like to create a new task for: {task}"
            confirmation = self.ui.get_user_confirmation(confirmation_msg)
            if confirmation:
                self.create_task(task)
        else:
            self.view_task(task)
        self.ui.print("")

        confirmation_msg = f"Task: [green]{task}[/green] \nDo you want to proceed?"
        confirmation = self.ui.get_user_confirmation(confirmation_msg)
         
        if confirmation:
            result = self.execution_engine.execute(task)
            self.ui.print_markdown(result)
            if int(result) != 0:
                while result != 0:
                    confirmation_msg = f"Would you like to update the task: {task} ?"
                    confirmation = self.ui.get_user_confirmation(confirmation_msg)
                    if confirmation:
                        self.delete_task(task)
                        self.create_task(task)
                        result = self.execution_engine.execute(task)
                    else:
                        break

    def delete_task(self,task=''):
        task = self.args.task
        if self.ansible_mgr.delete_config(task):
            self.ui.print_panel(f"[green]Deleted task: {task}[/green]")
        else:
            self.ui.print_panel(f"[red]Delete failed for task: {task}[/red]")

    def update_task(self):
        # view existin playbook
        task = self.args.task
        self.view_task(task)
        conf = self.ui.get_user_confirmation(f"\n Are you sure you want to update the existing task: {task} ?")
        if conf:
            self.delete_task(task)
            self.create_task(task)

def main():
    ops = Ops()
    ops.execute_command()

if __name__ == "__main__":
    main()