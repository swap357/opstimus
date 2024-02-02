from colorama import Fore, Style

from openai import OpenAI
from typing import List
from pydantic import Field
import instructor
from instructor import OpenAISchema
from opstimus.utils import utils
from opstimus.utils.user_interface import UserInterface
import subprocess
import json

class GPTAPIInterface:
    def __init__(self) -> None:
        self.client = instructor.patch(OpenAI())
        self.ui = UserInterface()

    def check_playbook_syntax(self,playbook):
        fpath = '/tmp/pb.yml'
        print(type(playbook))
        playbook_content = playbook["playbook_content"]
        print(playbook_content)
        with open(fpath,'w') as f:
            f.write(playbook_content)
            result = subprocess.run(['ansible-playbook', '--syntax-check', fpath], capture_output=True, text=True)
            if result.returncode == 0:
                print("Syntax check passed")
            else:
                print(f"Syntax check failed with error:\n{result.stderr}")
        return playbook_content

    def search_playbook(self,manifest,task):
        
        tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "check_playbook_syntax",
                        "description": "Use this function to check ansible playbook syntax. Input should be a fully formed ansible playbook yml.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "playbook": {
                                    "type": "object",
                                    "description": f"""
                                            Ansible playbook to achieve task specified on user's query.
                                            The response should be returned JSON using these keys -
                                            playbook_name: should be short one word, unix-dev-friendly string name of playbook. eg. sysinfo. If needed you can combine 2 short words. eg. getstats
                                            playbook_description: this description of playbook will be used to index and search matching playbook when fuzzy query is provided.
                                            playbook_content: valid ansible playbook yml content
                                            """,
                                }
                            },
                            "required": ["playbook"],
                        },
                    }
                }
            ]
        data = f"Manifest of tasks: {manifest} \
            >> to search for: {task}"
        
        system_msg = f"""
                    You are world-class ansible dev and linux, server management expert.
                    """
        user_msg = f"""
                    user query: {task}
                    Do not include any explanations, only provide a  RFC8259 compliant JSON response  following this format without deviation.
                    [{{
                        'playbook_name': 'short one word, unix-dev-friendly string name of playbook. eg. sysinfo. or combine 2 short words. eg. getstats',
                        'playbook_description': 'description of playbook optimized for indexing and search to find matching playbook when fuzzy query is provided',
                        'playbook_content': 'Valid ansible playbook yml. Try and use in-built libraries and tools as much as possible for playbook.'
                    }}]
                    The JSON response:
                    """
        messages = []
        messages.append({"role": "system", "content": system_msg})
        messages.append({"role": "user", "content": user_msg})
        chat_response = utils.chat_completion_request(messages)
        assistant_message = chat_response.choices[0].message
        self.ui.print_python(assistant_message.content)
        json_string = json.dumps(assistant_message.content)
        response = json.loads(json_string)
        # playbook_content = assistant_message.content["playbook_content"]
        self.ui.print_yaml(response[0]['playbook_content'])
        # assistant_message.content = str(assistant_message.tool_calls[0].function)
        messages.append({"role": assistant_message.role, "content": assistant_message.content})
        # if assistant_message.tool_calls:
        #     results = self.check_playbook_syntax(assistant_message)
        #     messages.append({"role": "function", "tool_call_id": assistant_message.tool_calls[0].id, "name": assistant_message.tool_calls[0].function.name, "content": results})

        return completion

    def create_playbook(self,task):
        # Mocked code to create playbook
        print(f"{Fore.GREEN}Creating playbook...{Style.RESET_ALL}")
        return "pb1", "description", "playbook_content"+task