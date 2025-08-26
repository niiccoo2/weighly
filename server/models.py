from pydantic import BaseModel
from typing import List, Optional

class Weight(BaseModel):
    id: Optional[int] = None
    name: str
    weight: float
    type: str
    time: str

class Summed_Weight(BaseModel):
    name: str
    weight: float
    type: Optional[str] = None

class Event(BaseModel):
    event_id: int
    name: str
    custom_url: Optional[str] = None

class Summary(BaseModel):
    event: Event
    totals: List[Summed_Weight]