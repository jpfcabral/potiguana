from langchain_openai import ChatOpenAI

from src.agents.tools import tools

llm = ChatOpenAI(model="gpt-4o-mini")

from typing import Annotated, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
    Você é o mascote da UFRN responsável por responder dúvidas sobre
    questões acadêmicas. Responda somente perguntas relacionadas a
    esse contexto.
    """,
)
