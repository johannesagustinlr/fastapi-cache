from pydantic import BaseModel
from typing import List


class CreateInput(BaseModel):

    list_1: List[str]
    list_2: List[str]
