import os

from langchain_aws.embeddings import BedrockEmbeddings
from langchain_qdrant import QdrantVectorStore
from loguru import logger
from qdrant_client import QdrantClient


class SemanticRouter:
    def __init__(
        self,
        qdrant_host: str = os.environ["VECTOR_STORE_URL"],
        api_key: str = os.environ["VECTOR_STORE_API_KEY"],
        collection_name: str = "utterances",
    ):
        self.qdrant_client = QdrantClient(url=qdrant_host, api_key=api_key)
        self.embedding = BedrockEmbeddings()

        self.collection_name = collection_name

        self.vector_store = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=self.collection_name,
            embedding=self.embedding,
        )

    def add_utterance(self, utterance, route):
        """Add an utterance and its associated route to the Qdrant collection."""
        self.vector_store.add_texts(
            texts=[utterance], metadatas=[{"route": route, "uterrance": utterance}]
        )

    def get_route_details(self, query, k: int = 10):
        """Retrieve routes, utterances, and scores for a given query without filtering by threshold."""
        results = self.vector_store.similarity_search_with_relevance_scores(
            query=query, k=k
        )
        detailed_results = [
            (res.metadata["route"], res.metadata["uterrance"], score)
            for res, score in results
        ]
        return detailed_results

    def get_route(self, query, threshold: float = 0.9):
        """Retrieve the most relevant route for a given query based on the highest score exceeding the threshold."""
        detailed_results = self.get_route_details(query=query)

        # Filter results based on threshold
        filtered_results = [
            (route, utterance, score)
            for route, utterance, score in detailed_results
            if score >= threshold
        ]

        if not filtered_results:
            return None

        # Find the route with the highest score
        best_result = max(filtered_results, key=lambda x: x[2])

        logger.info(
            f"Router best score | query: {query}, route: {best_result[0]}, utterance: {best_result[1]}, score: {best_result[2]}"
        )
        return best_result[0]  # Return the route of the best result
