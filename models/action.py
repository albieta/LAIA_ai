from typing import List
from pydantic import BaseModel

class ActionModel(BaseModel):
    name: str = ''
    description: str = ''
    inputs: List[str] = []
    code: str = ''