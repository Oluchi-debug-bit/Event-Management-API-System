from fastapi import APIRouter, HTTPException
from schemas.user import User, UserCreate
from services.user import create_user, get_users, deactivate_user

router = APIRouter()

@router.post("/", response_model=User)
def create(user: UserCreate):
    return create_user(user)

@router.get("/", response_model=list[User])
def list_users():
    return get_users()

@router.put("/{user_id}/deactivate", response_model=User)
def deactivate(user_id: int):
    user = deactivate_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
