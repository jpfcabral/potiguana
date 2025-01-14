import json

import boto3


class BedrockRerank:
    def rerank(
        self,
        query: str,
        documents: list[str],
        top_k=3,
        model: str = "amazon.rerank-v1:0",
        client=None,
    ):
        """ """

        if not client:
            client = boto3.client("bedrock-runtime")

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
