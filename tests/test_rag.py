import logging
import os

from esynergy_open_rag.components.embeddings.embedding import Embedding
from esynergy_open_rag.components.llms.llm import LLM
from esynergy_open_rag.components.rags.rag import RAG
from esynergy_open_rag.components.retrievers.retriever import Retriever
from esynergy_open_rag.config import chain


class TestRag:
    def test_rag_chain(self):
        logging.info(chain.invoke("summary of the datamesh project"))

    def test_rag_step_by_step(self):
        model_name = os.getenv("LLM_MODEL")
        embedding_model_name = os.getenv("EMBEDDING_MODEL")
        model = LLM(model_type="bedrock", model_name=model_name).llm
        embeddings = Embedding(model_type="bedrock", model_name=embedding_model_name).embedding

        retriever_name = "astradb"  # Replace with the desired retriever name
        retriever = Retriever().get_retriever(retriever_name, embeddings)

        chain = RAG(model, retriever).chain
        response = chain.invoke("summary of the datamesh project")
        logging.info(response)
