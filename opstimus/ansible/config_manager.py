from colorama import Fore, Style
import instructor
from openai import OpenAI
from pydantic import BaseModel
import yaml
from rich.console import Console

from opstimus.ansible.ansible_config import AnsibleConfig
from opstimus.base_config_manager import BaseConfigManager
from opstimus.ansible.utils import system_msg
from opstimus.utils.file_storage import FileStorage
from opstimus.utils.user_interface import UserInterface

client = instructor.patch(OpenAI())

class AnsibleManager(BaseConfigManager):
    
    def __init__(self, file_storage: FileStorage):
        super().__init__(file_storage)
        self.ui = UserInterface()
        self.console = Console()

    def get_config(self, name):
        content = self.file_storage.get_file_content(name)
        if content:
            return content
        else:
            # print("Error loading playbook.")
            return None

    def create_config(self, user_query):
        try:
            
            with self.console.status('Calling GPT...') as status:
                new_playbook = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    response_model=AnsibleConfig,
                    messages=[
                        {
                            "role": "system",
                            "content": system_msg,
                        },
                        {
                            "role": "user",
                            "content": f"""
                                        {user_query}
                                        """
                        }
                        ]
                )
            return new_playbook.name, new_playbook.description, new_playbook.content
        except Exception as e:
            raise e
            return None,None,None

    def save_config(self, playbook_name, playbook_description, playbook_data):
        content = yaml.safe_dump([playbook_data], default_flow_style=False, sort_keys=False, explicit_start=True, indent=2, width=80)
        self.file_storage.store_file(playbook_name, playbook_description, content)

    def validate_config(self, config_data):
        # Simple validation example: check if it's valid YAML
        try:
            yaml.safe_load(config_data)
            return True
        except yaml.YAMLError as exc:
            print(exc)
            return False
    
    def delete_config(self, name):
        if self.file_storage.get_file_content(name):
            self.file_storage.delete_file(name)
            return True
        else:
            return False