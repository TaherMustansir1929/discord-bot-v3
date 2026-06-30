from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage

from src.prompts.roast import roast_prompt

load_dotenv()


async def roast_agent(
    user_prompt: str, model: ChatGoogleGenerativeAI | ChatGroq
) -> str:
    agent = create_agent(
        model=model,
        system_prompt=roast_prompt,
    )
    response = await agent.ainvoke({"messages": [HumanMessage(content=user_prompt)]})

    if isinstance(response["messages"][-1], AIMessage):
        return response["messages"][-1].content[0]["text"]
    return "Something went wrong with the agent response."
