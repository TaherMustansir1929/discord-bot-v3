from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from src.services.speech import generate_speech

router = APIRouter(prefix="/speech", tags=["speech"])

class SpeechRequest(BaseModel):
    text: str
    voice: str

@router.post("/")
def speech_endpoint(req: SpeechRequest):
    try:
        audio_bytes = generate_speech(req.text, req.voice)
        return Response(content=audio_bytes, media_type="audio/wav")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in speech_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
