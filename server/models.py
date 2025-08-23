from pydantic import BaseModel

class Weight(BaseModel):
    id: int
    name: str
    weight: float
