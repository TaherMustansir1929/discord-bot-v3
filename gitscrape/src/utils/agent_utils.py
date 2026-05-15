import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import SecretStr

load_dotenv()

GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")

_model_groq: ChatGroq | None = None


def get_groq_model(model=GROQ_MODEL_NAME, temperature=0.7) -> ChatGroq:
    global _model_groq
    if _model_groq is not None:
        return _model_groq

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to your environment or .env file."
        )

    _model_groq = ChatGroq(
        model=model,
        temperature=temperature,
        api_key=SecretStr(api_key),
    )
    return _model_groq
