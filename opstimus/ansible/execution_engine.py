import subprocess
import os
from rich.console import Console
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible import context
import ansible.constants as C
from ansible.module_utils.common.collections import ImmutableDict

from opstimus.utils.user_interface import UserInterface
from opstimus.base_execution_engine import BaseExecutionEngine

class CustomCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = UserInterface()
        self.status = None
        self.console = Console()
        
    def v2_playbook_on_task_start(self, task, **kwargs):
        self.status = self.console.status(f"[bold blue]Starting task: {task}...", spinner="dots")

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        
        self.ui.print_panel(f"[green]✔️ {host} - {result._task} completed[/green]")
        if 'stdout' in result._result:
            self.ui.print_python(result._result['msg'])
        if 'stderr' in result._result and result._result['stderr']:
            self.ui.print("STDERR:")
            self.ui.print_yaml(result._result['stderr'])
        if 'msg' in result._result:
            self.ui.print_python(result._result['msg'])
        print()
    
    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host
        self.ui.print_panel(f"[red] ❌ {host} - {result._task} failed[/red]")
        if 'msg' in result._result:
            self.ui.print_python(result._result['msg'])

class AnsibleExecutionEngine(BaseExecutionEngine):
    ANSIBLE_MODULE_PATH = '/home/ubuntu/.venv/lib/python3.10/site-packages/ansible'

    def __init__(self, playbook_directory):
        """
        Initializes the AnsibleExecutionEngine with the directory where playbooks are stored.
        
        Parameters:
            playbook_directory (str): The directory where Ansible playbooks are located.
        """
        self.playbook_directory = playbook_directory
    
    def get_playbook_path(self, playbook_name):
        """
        Get the full file path of a playbook.
        
        Parameters:
            playbook_name (str): The name of the playbook.
            
        Returns:
            str: The full path to the playbook file.
        """
        return os.path.join(self.playbook_directory, playbook_name + '.yml')
    
    def execute(self, playbook_name, *args, **kwargs):
        """
        Execute an Ansible playbook.
        
        Parameters:
            playbook_name (str): The name of the playbook to be executed.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
            
        Returns:
            result (dict): The result of the playbook execution.
        """
        playbook_path = self.get_playbook_path(playbook_name)
        if not os.path.exists(playbook_path):
            return {'success': False, 'message': f'Playbook {playbook_name} does not exist.'}

        loader = DataLoader()
        inventory = InventoryManager(loader=loader, sources='localhost,')
        variable_manager = VariableManager(loader=loader, inventory=inventory)
        context.CLIARGS = ImmutableDict(connection='local', module_path=[self.ANSIBLE_MODULE_PATH,'/usr/share/ansible'], forks=10, become=None,
                                        become_method=None, become_user=None, check=False, diff=False, syntax=False, start_at_task=None)
        playbook_executor = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, passwords=dict(vault_pass='secret'))
        playbook_executor._tqm._stdout_callback = CustomCallback()
        result = playbook_executor.run()
        return result
    
    def validate_execution(self, playbook_name):
        """
        Validate if a playbook can be executed.
        
        Parameters:
            playbook_name (str): The name of the playbook to be validated.
            
        Returns:
            is_valid (bool): True if the playbook exists and can be executed, False otherwise.
        """
        playbook_path = self.get_playbook_path(playbook_name)
        return os.path.exists(playbook_path)
