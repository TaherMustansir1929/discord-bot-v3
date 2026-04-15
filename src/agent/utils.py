import os
from pydantic import SecretStr

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI


_model_groq: ChatGroq | None = None
_model_google: ChatGoogleGenerativeAI | None = None


def get_groq_model(model="llama-3.3-70b-versatile", temperature=0.7) -> ChatGroq:
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


def get_google_model(
    model="gemini-3-flash-preview", temperature=0.7
) -> ChatGoogleGenerativeAI:
    global _model_google
    if _model_google is not None:
        return _model_google

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Add it to your environment or .env file."
        )

    _model_google = ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        google_api_key=SecretStr(api_key),
    )
    return _model_google
