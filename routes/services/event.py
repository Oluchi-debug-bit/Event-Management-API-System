from schemas.event import Event, EventCreate

events = []
event_id_counter = 1

def create_event(data: EventCreate) -> Event:
    global event_id_counter
    event = Event(id=event_id_counter, **data.dict())
    events.append(event)
    event_id_counter += 1
    return event

def get_events():
    return events

def close_event(event_id: int):
    for event in events:
        if event.id == event_id:
            event.is_open = False
            return event
    return None
