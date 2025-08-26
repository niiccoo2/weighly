from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from typing import List
from models import Weight, Summed_Weight, Summary
from database import DB
import markdown2

router = APIRouter()

db = DB()

@router.get("/", response_class=HTMLResponse)
def give_guide(): # Nico this should just give the readme so they can see it if they go to it.
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
            html_content = markdown2.markdown(content, extras=["fenced-code-blocks"])
            return html_content
    except FileNotFoundError:
        return "Welcome to the Weighly API. Please refer to the README.md file in the repo for more information. (404 readme error)"

@router.get("/{event}/entries", response_model=List[Weight])
def read_entries(event: str):
    return db.get_entries(event)

@router.get("/{event}/totals", response_model=List[Summed_Weight])
def read_totals(event: str):
    return db.get_sums(event)

@router.get("/{event}/total", response_model=float)
def read_total(event: str):
    return db.get_total(event)

@router.get("/{event}/summary", response_model=Summary)
def make_summary(event: str):
    return {
        "event": db.get_event_info(event),
        "totals": db.get_sums(event)
    }

@router.post("/{event}/add_weight")
async def save_weight_to_db(event: int, item: Weight):
    db.save_weight(event, item)
    return {
        "message": "Item saved successfully!",
        "item": item
    }

@router.get("/{event}") # This would not require an api key prob just tells you what event has the id
def get_event_from_id(event: str):
    return {
        "event": db.get_event_info(event),
    }
