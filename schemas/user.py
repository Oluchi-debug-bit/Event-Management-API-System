from pydantic import BaseModel, EmailStr

# This is the model used when returning user data (e.g., in a response)
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str  # e.g., "attendee", "organizer", "admin"

    class Config:
        orm_mode = True

# This is the model used when creating a new user (e.g., in a POST request)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # Let them choose or assign a role
