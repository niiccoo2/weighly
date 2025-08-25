from fastapi import APIRouter
from typing import List
from models import Weight, Summed_Weight, Summary
from database import get_entries, get_sums, get_event_info

router = APIRouter()

@router.get("/{event}/entries", response_model=List[Weight])
def read_entries(event: str):
    return get_entries(event)

@router.get("/{event}/totals", response_model=List[Summed_Weight])
def read_totals(event: str):
    return get_sums(event)

@router.get("/{event}/summary", response_model=Summary)
def make_summary(event: str):
    return {
        "event": get_event_info(event),
        "totals": get_sums(event)
    }