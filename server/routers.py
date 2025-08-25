from fastapi import APIRouter
from typing import List
from models import Weight, Summed_Weight
from database import get_entries, get_sums

router = APIRouter()

@router.get("/{event}/entries", response_model=List[Weight])
def read_weights(event: str):
    return get_entries(event)

@router.get("/{event}/totals", response_model=List[Summed_Weight])
def read_weights(event: str):
    return get_sums(event)

@router.get("/{event}/summary", response_model=List[Summed_Weight])
def read_weights(event: str):
    return get_sums(event)