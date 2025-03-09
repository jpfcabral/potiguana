import os

from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.tools.retriever import create_retriever_tool
from langchain_aws import BedrockEmbeddings, BedrockRerank
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from config.settings import settings

embeddings = BedrockEmbeddings()

qdrant_client = QdrantClient(
    location=settings.VECTOR_STORE_URL,
    api_key=settings.VECTOR_STORE_API_KEY,
)

bedrock_rerank = BedrockRerank(
    model_arn="arn:aws:bedrock:us-west-2::foundation-model/amazon.rerank-v1:0",
    top_n=20,
)


regulamento_vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="regulamento_dos_cursos_de_graduacao_da_UFRN",
    embedding=embeddings,
)

regulamento_retriever = ContextualCompressionRetriever(
    base_compressor=bedrock_rerank,
    base_retriever=regulamento_vector_store.as_retriever(search_kwargs={"k": 50}),
)

calendario_vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="calendario_universitario_2025",
    embedding=embeddings,
)

calendario_retriever = ContextualCompressionRetriever(
    base_compressor=bedrock_rerank,
    base_retriever=calendario_vector_store.as_retriever(search_kwargs={"k": 50}),
)


regulamentos_tool = create_retriever_tool(
    regulamento_retriever,
    "regulamentos_graducacao",
    "Artigos do Regulamento dos Cursos Regulares de Graduação",
)

calendario_tool = create_retriever_tool(
    calendario_retriever, "calendario_2025", "Calendário Universitário da UFRN 2025"
)

tools = [regulamentos_tool, calendario_tool]
