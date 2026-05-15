from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pydantic import BaseModel, Field

from src.prompts import QUERY_EXPANSION_PROMPT
from src.utils import get_groq_model


class Queries(BaseModel):
    """List of queries to search for."""

    queries: list[str] = Field(description="List of relevant queries to search for")


async def query_expansion_agent(query: str) -> list[str]:

    agent = create_agent(
        model=get_groq_model(),
        response_format=Queries,
    )

    result = agent.invoke(
        {"messages": [HumanMessage(content=QUERY_EXPANSION_PROMPT.format(query=query))]}
    )
    return result["structured_response"].queries
