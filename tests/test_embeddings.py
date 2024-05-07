import os

from dotenv import load_dotenv

from esynergy_open_rag.components.embeddings.embedding import Embedding

load_dotenv()


class TestEmbedding:
    # how to run a pytest
    # pytest tests/test_llm.py
    def test_embeddings(self):
        embedding_model_name = os.getenv("EMBEDDING_MODEL")
        sentence = "Hello World"
        data = Embedding(model_type="bedrock", model_name=embedding_model_name).embedding.embed_query(sentence)
        assert len(data) == 1536
