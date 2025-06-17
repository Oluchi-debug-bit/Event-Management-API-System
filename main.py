# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# In-memory data storage
users = []
events = []
speakers = [
    {"id": 1, "name": "Alice", "topic": "AI Innovations"},
    {"id": 2, "name": "Bob", "topic": "Blockchain Basics"},
    {"id": 3, "name": "Charlie", "topic": "Cybersecurity Trends"},
]
registrations = []

# Pydantic models
class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

class Event(BaseModel):
    id: int
    title: str
    location: str
    date: datetime
    is_open: bool = True

class Registration(BaseModel):
    id: int
    user_id: int
    event_id: int
    registration_date: datetime
    attended: bool = False

# User Endpoints
@app.post("/users/", response_model=User)
def create_user(user: User):
    users.append(user)
    return user

@app.get("/users/", response_model=List[User])
def read_users():
    return users

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    for idx, existing_user in enumerate(users):
        if existing_user.id == user_id:
            users[idx] = user
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    for idx, existing_user in enumerate(users):
        if existing_user.id == user_id:
            return users.pop(idx)
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users/{user_id}/deactivate")
def deactivate_user(user_id: int):
    for user in users:
        if user.id == user_id:
            user.is_active = False
            return {"message": "User deactivated"}
    raise HTTPException(status_code=404, detail="User not found")

# Event Endpoints
@app.post("/events/", response_model=Event)
def create_event(event: Event):
    events.append(event)
    return event

@app.get("/events/", response_model=List[Event])
def read_events():
    return events

@app.put("/events/{event_id}", response_model=Event)
def update_event(event_id: int, event: Event):
    for idx, existing_event in enumerate(events):
        if existing_event.id == event_id:
            events[idx] = event
            return event
    raise HTTPException(status_code=404, detail="Event not found")

@app.delete("/events/{event_id}", response_model=Event)
def delete_event(event_id: int):
    for idx, existing_event in enumerate(events):
        if existing_event.id == event_id:
            return events.pop(idx)
    raise HTTPException(status_code=404, detail="Event not found")

@app.post("/events/{event_id}/close")
def close_event(event_id: int):
    for event in events:
        if event.id == event_id:
            event.is_open = False
            return {"message": "Event registration closed"}
    raise HTTPException(status_code=404, detail="Event not found")

# Registration Endpoints
@app.post("/registrations/", response_model=Registration)
def register_user(registration: Registration):
    user = next((u for u in users if u.id == registration.user_id and u.is_active), None)
    event = next((e for e in events if e.id == registration.event_id and e.is_open), None)
    
    if not user:
        raise HTTPException(status_code=400, detail="User is not active or does not exist")
    if not event:
        raise HTTPException(status_code=400, detail="Event is not open or does not exist")
    if any(r for r in registrations if r.user_id == registration.user_id and r.event_id == registration.event_id):
        raise HTTPException(status_code=400, detail="User already registered for this event")
    
    registrations.append(registration)
    return registration

@app.put("/registrations/{registration_id}/attend")
def mark_attendance(registration_id: int):
    for registration in registrations:
        if registration.id == registration_id:
            registration.attended = True
            return {"message": "Attendance marked"}
    raise HTTPException(status_code=404, detail="Registration not found")

@app.get("/registrations/user/{user_id}", response_model=List[Registration])
def get_user_registrations(user_id: int):
    return [r for r in registrations if r.user_id == user_id]

@app.get("/registrations/", response_model=List[Registration])
def get_all_registrations():
    return registrations

