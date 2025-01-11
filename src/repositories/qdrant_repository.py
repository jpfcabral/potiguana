from typing import List

from langchain.schema import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from config.settings import settings


class QDrantRepository:
    """
    Repository for interacting with a Qdrant vector store.

    This class handles the initialization of the Qdrant client and provides methods
    for searching documents based on similarity.
    """

    def __init__(
        self,
        embeddings,
        url: str = settings.VECTOR_STORE_URL,
        api_key: str = settings.VECTOR_STORE_API_KEY,
    ):
        """
        Initializes the QDrantRepository with the provided embeddings and Qdrant client.

        Args:
            embeddings: The embeddings model to use for vectorizing queries and documents.
            url (str): The URL of the Qdrant vector store. Defaults to settings.VECTOR_STORE_URL.
            api_key (str): The API key for authenticating with Qdrant. Defaults to settings.VECTOR_STORE_API_KEY.
        """
        client = QdrantClient(location=url, api_key=api_key)

        self.vector_store = QdrantVectorStore(
            client=client, collection_name="regulamento-semantic", embedding=embeddings
        )

    def search(self, query, k: int = 50) -> List[Document]:
        """
        Searches for documents in the vector store that are similar to the query.

        Args:
            query (str): The search query.
            k (int): The number of top results to return. Defaults to 50.

        Returns:
            List[Document]: A list of documents that are most similar to the query.
        """

        doc_list = self.vector_store.similarity_search(query=query, k=k)
        return doc_list
