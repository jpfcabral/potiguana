import uvicorn
from fastapi import FastAPI

from models.question import QuestionRequest
from services.chatbot_service import ChatbotService

app = FastAPI()


@app.post("/")
def chat(request: QuestionRequest):
    """Triggers chatbot pipeline"""
    query = request.question
    chat_id = request.chat_id
    chatbot = ChatbotService()
    return chatbot.answer(query=query, chat_id=chat_id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
