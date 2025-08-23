from fastapi import APIRouter
from typing import List
from models import Weight
from database import get_weights_by_group

router = APIRouter()

@router.get("/weights/{group}", response_model=List[Weight])
def read_weights(group: str):
    return get_weights_by_group(group)
