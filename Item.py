from typing import Any
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float