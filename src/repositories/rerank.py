import json

import boto3


class BedrockRerank:
    """
    Service for reranking documents based on a query using AWS Bedrock models.

    This class handles interaction with the Bedrock runtime to rerank a list of documents
    according to their relevance to a given query.
    """

    def rerank(
        self,
        query: str,
        documents: list[str],
        top_k=3,
        model: str = "amazon.rerank-v1:0",
        client=None,
    ):
        """
        Reranks a list of documents based on their relevance to the query.

        Args:
            query (str): The query string to compare against the documents.
            documents (list[str]): A list of documents to be reranked. Can include dictionaries serialized to strings.
            top_k (int): The number of top results to return. Defaults to 3.
            model (str): The model identifier for the reranking operation. Defaults to 'amazon.rerank-v1:0'.
            client (boto3.client, optional): An optional boto3 client instance. If not provided, a new client will be created.

        Returns:
            list[str]: A list of reranked documents in descending order of relevance.
        """

        if not client:
            client = boto3.client("bedrock-runtime", region_name="us-west-2")

        # Serialize dictionaries to JSON strings to simulate mixed inputs
        serialized_documents = [
            json.dumps(doc) if isinstance(doc, dict) else doc for doc in documents
        ]

        metadata = {}

        if model.startswith("cohere"):
            metadata["api_version"] = 2

        body = json.dumps(
            {
                "query": query,
                "documents": serialized_documents,
                "top_n": top_k,
                **metadata,
            }
        )
        # Invoke the Bedrock model
        response = client.invoke_model(
            modelId=model,
            accept="application/json",
            contentType="application/json",
            body=body,
        )
        response_body = json.loads(response.get("body").read())
        matching_indices = [result["index"] for result in response_body["results"]]
        matching_documents = [documents[i] for i in matching_indices]

        return matching_documents
