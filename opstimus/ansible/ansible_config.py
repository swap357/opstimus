from pydantic import BaseModel, validator
from typing import Any, Dict
import yaml

class AnsibleConfig(BaseModel):
    name: str
    description: str
    content: Any