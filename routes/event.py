from fastapi import APIRouter, HTTPException
from schemas.event import Event, EventCreate
from services.event import create_event, get_events, close_event

router = APIRouter()

@router.post("/", response_model=Event)
def create(event: EventCreate):
    return create_event(event)

@router.get("/", response_model=list[Event])
def list_events():
    return get_events()

@router.put("/{event_id}/close", response_model=Event)
def close(event_id: int):
    event = close_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
