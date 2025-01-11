from fastapi import FastAPI

from services.chatbot_service import ChatbotService

app = FastAPI()


@app.get("/")
def chat(query: str):
    """Triggers chatbot pipeline"""
    chatbot = ChatbotService()
    return chatbot.answer(query=query)
