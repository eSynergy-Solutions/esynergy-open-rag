import os

from dotenv import load_dotenv

from esynergy_open_rag.components.embeddings.embedding import Embedding
from esynergy_open_rag.components.llms.llm import LLM
from esynergy_open_rag.components.rags.rag import RAG
from esynergy_open_rag.components.retrievers.retriever import Retriever

load_dotenv()

# os.environ['LANGCHAIN_TRACING_V2'] = 'true'
# os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
# os.environ['LANGCHAIN_ENDPOINT'] = os.getenv('LANGCHAIN_ENDPOINT')
# os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')

llm = LLM(model_type=os.getenv("MODEL_TYPE"), model_name=os.getenv("LLM_MODEL")).llm

embedding_model_name = os.getenv("EMBEDDING_MODEL")
embeddings = Embedding(model_type="bedrock", model_name=embedding_model_name).embedding
retriever = Retriever().get_retriever(os.getenv("RETRIEVER_NAME"), embeddings)
chain = RAG(retriever=retriever, llm=llm).chain
