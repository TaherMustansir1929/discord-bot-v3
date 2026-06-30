import os
from groq import Groq
from fastapi import HTTPException

def generate_speech(text: str, voice: str) -> bytes:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not found in environment variables.")
        
    client = Groq(api_key=api_key)
    try:
        response = client.audio.speech.create(
            model="canopylabs/orpheus-v1-english",
            voice=voice,
            input=text,
            response_format="wav",
        )
        return response.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
