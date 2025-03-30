from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from pymongo import MongoClient

from agents.tools import tools
from checkpointer.custom_checkpointer import CustomCheckpointer
from config.prompt import PROMPT
from config.settings import settings

mongodb_client = MongoClient(settings.MONGO_URI)
checkpointer = CustomCheckpointer(client=mongodb_client, ttl=600)

llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=PROMPT,
    checkpointer=checkpointer,
)
