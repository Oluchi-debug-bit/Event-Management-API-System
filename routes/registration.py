from fastapi import APIRouter, HTTPException
from services.registration import register_user, mark_attendance, get_all_registrations, get_user_registrations, get_users_attended
from schemas.registration import Registration
from schemas.user import User

router = APIRouter()

@router.post("/", response_model=Registration)
def register(user_id: int, event_id: int):
    reg = register_user(user_id, event_id)
    if not reg:
        raise HTTPException(status_code=400, detail="Invalid registration")
    return reg

@router.put("/{reg_id}/attend", response_model=Registration)
def attend(reg_id: int):
    reg = mark_attendance(reg_id)
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")
    return reg

@router.get("/", response_model=list[Registration])
def list_all():
    return get_all_registrations()

@router.get("/user/{user_id}", response_model=list[Registration])
def list_by_user(user_id: int):
    return get_user_registrations(user_id)

@router.get("/attendees", response_model=list[User])
def attendees():
    return get_users_attended()
