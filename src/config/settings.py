from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    VECTOR_STORE_URL: str
    VECTOR_STORE_API_KEY: str
    TELEGRAM_API_TOKEN: str
    MONGO_URI: str


settings = Settings()
