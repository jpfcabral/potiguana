import random
from time import sleep

from langchain.prompts import PromptTemplate
from langchain_aws import BedrockEmbeddings, ChatBedrock
from langchain_core.messages import BaseMessage
from loguru import logger

from config.prompt import GENERATOR_PROMPT
from repositories.qdrant_repository import QDrantRepository
from repositories.rerank import BedrockRerank
from repositories.semantic_router import SemanticRouter
from services.telegram_service import DynamoDBRepository

random.seed(21)


class ChatbotService:
    """
    Service for interacting with a chatbot model hosted on AWS Bedrock.

    This service handles context retrieval, reranking, and communication with a language model
    to generate responses based on user queries.
    """

    def __init__(
        self,
        model_name: str = "amazon.nova-micro-v1:0",
        repository: DynamoDBRepository = DynamoDBRepository(),
    ):
        """
        Initializes the ChatbotService with the specified model.

        Args:
            model_name (str): The identifier of the LLM model to use. Defaults to 'amazon.nova-micro-v1:0'.
        """
        self.repository = repository

        self.llm = ChatBedrock(model_id=model_name, temperature=0.0, region="us-east-1")
        self.embedding = BedrockEmbeddings()
        self.vector_store = QDrantRepository(embeddings=self.embedding)
        self.reranker = BedrockRerank()
        self.semantic_router = SemanticRouter()

    def answer(self, query: str):
        """
        Provides an answer to a user query using retrieved and reranked contexts.

        Args:
            query (str): The user's input question or query.

        Returns:
            dict: The response generated by the language model, represented as a dictionary.
        """

        route: str = self.semantic_router.get_route(query)

        if route == "greetings":
            return {"content": "Olá, eu sou a potiguana"}

        if route == "farewells":
            return {"content": "Até logo"}

        # Retrieve and rerank contexts
        context_docs = self.vector_store.search(query=query)
        contexts = [c.page_content for c in context_docs]
        reranked_contexts = self.reranker.rerank(
            query=query, documents=contexts, top_k=20
        )

        # Generate prompt
        prompt_template = PromptTemplate.from_template(GENERATOR_PROMPT)
        formatted_contexts = "\n".join(reranked_contexts)
        prompt = prompt_template.format(pergunta=query, contexto=formatted_contexts)

        # Invoke LLM
        response: BaseMessage = self.invoke_llm_with_backoff(
            llm=self.llm, prompt=prompt
        )

        response_dict = response.dict()
        self.repository.insert(data=response_dict, table_name="responses")

        logger.debug(f"LLM Response: {response}")

        return response_dict

    def invoke_llm_with_backoff(self, llm: ChatBedrock, prompt, max_retries=5):
        """
        Invokes the language model with exponential backoff for handling throttling errors.

        Args:
            llm (ChatBedrock): The language model client.
            prompt (str): The prompt to send to the model.
            max_retries (int): Maximum number of retries for throttling errors. Defaults to 5.

        Returns:
            BaseMessage: The response from the language model.

        Raises:
            Exception: If the maximum number of retries is reached.
        """
        retries = 0
        while retries < max_retries:
            try:
                return llm.invoke(prompt)
            except Exception as exc:
                print(exc)
                retries += 1
                wait_time = random.uniform(  # nosec
                    2**retries, 2**retries + 5
                )  # Exponential backoff
                print(f"Throttling error. Retrying in {wait_time:.2f} seconds...")
                sleep(wait_time)

        raise Exception("Max retries reached, could not invoke model.")
