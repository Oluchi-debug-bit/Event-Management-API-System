from fastapi import APIRouter
from services.speaker import get_speakers
from schemas.speaker import Speaker

router = APIRouter()

@router.get("/", response_model=list[Speaker])
def list_speakers():
    return get_speakers()
