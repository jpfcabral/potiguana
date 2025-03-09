import uvicorn
from fastapi import FastAPI

from services.chatbot_service import ChatbotService

app = FastAPI()


@app.get("/")
def chat(query: str):
    """Triggers chatbot pipeline"""
    chatbot = ChatbotService()
    return chatbot.answer(query=query)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
