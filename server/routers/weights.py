from fastapi import APIRouter
from typing import List
from models import Weight
from database import get_weights

router = APIRouter()

@router.get("/weights/{event}", response_model=List[Weight])
def read_weights(event: str):
    return get_weights(event)
