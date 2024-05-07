import os

from esynergy_open_rag.components.embeddings.embedding import Embedding
from esynergy_open_rag.components.retrievers.retriever import Retriever


def test_retriever():
    embedding_model_name = os.getenv("EMBEDDING_MODEL")
    embeddings = Embedding(model_type="bedrock", model_name=embedding_model_name).embedding
    query = "prepare a draft on the projects by northern trust"
    retriever_name = "astradb"  # Replace with the desired retriever name
    retriever = Retriever().get_retriever(retriever_name, embeddings)
    res = retriever.get_relevant_documents(query)
    assert len(res) > 0
