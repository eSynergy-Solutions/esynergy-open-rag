import logging
from typing import Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# from components.embeddings.embedding import Embedding
from esynergy_open_rag.components.llms.llm import LLM


class RAG:
    """
    The Retriever-And-Generator (RAG) class is designed to use a retriever model to fetch relevant
    documents and then generate answers based on these documents. The RAG system can operate in
    different modes depending on the specified 'rag_type'. This allows for flexibility in how
    documents are sourced and used in the generation of answers.

    Attributes:
        model (LLM): The language model used for generating answers.
        retriever: The model or system used to retrieve documents that provide context for the language model.
        rag_type (Optional[str]): The mode of operation for the RAG system which can be 'with_source',
            'from_docs', or 'no_source'.
        chain: The runnable chain that processes input to generate output based on the specified 'rag_type'.

    Args:
        llm (LLM): The language model instance used for answer generation.
        retriever: The retriever instance used for fetching documents relevant to a given query.
        rag_type (Optional[str]): Specifies the mode of RAG operation, defaults to 'with_source'.
    """

    def __init__(self, llm: LLM, retriever, rag_type: Optional[str] = "with_source"):
        self.model = llm
        self.retriever = retriever
        self.rag_type = rag_type
        self.chain = self._load_chain()

    def _load_chain(self):
        """
        Initializes the appropriate processing chain based on the 'rag_type'. This method selects
        the specific operational mode of the RAG system, whether it incorporates document sources
        into the response, uses documents directly, or does not use external sources at all.

        Returns:
            Runnable: The configured processing chain ready for invocation.
        """
        if self.rag_type == "with_source":
            logging.info("Loading from {self.rag_type}")
            return self._load_with_source()
        elif self.rag_type == "from_docs":
            logging.info("Loading from {self.rag_type}")
            return self._load_from_docs()
        elif self.rag_type == "no_source":
            logging.info("Loading from {self.rag_type}")
            return self._load_no_source()
        else:
            logging.info("Tried loading from {self.rag_type}, not supported.")
            raise ValueError("Model type not supported")

    def _load_with_source(self):
        """
        Configures the processing chain for the 'with_source' mode. In this mode, the system uses
        a retriever to fetch documents relevant to the query, and then these documents along with
        the query are fed into a language model to generate a response.

        Returns:
            Runnable: The processing chain configured for the 'with_source' mode.
        """
        # get template from env
        template = """
            Human: Greet the user politely, is its a generic conversation. If you don't know the answer, just say
            that you don't know, don't try to make up an answer. Please make sure the answer is short and precise.
            Always Answer with respect to the context or with respect to the documents given in the context.
            Note that you are a Copilot of Esynergy Solutions, that helps the user in answer queries on BID in both
            Public and Private Sector. Also if not enought context please do not mention Unfortunately
            I do not have enough context, instead answer with the context available.
            Context: {context}
            Question: {question}
            Assistant:
            """
        prompt = ChatPromptTemplate.from_template(template)

        def format_docs(docs):
            try:
                return "\n\n".join(doc.page_content for doc in docs)
            except Exception:
                logging.error("No data found in the context\n\n")
                logging.error(Exception)
                return "NoData"

        rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
            | prompt
            | self.model
            | StrOutputParser()
        )

        rag_chain_with_source = RunnableParallel({"context": self.retriever, "question": RunnablePassthrough()}).assign(
            answer=rag_chain_from_docs
        )

        return rag_chain_with_source

    def _load_from_docs(self):
        """
        Placeholder method for the 'from_docs' mode. In this mode, the system would typically
        use a set of pre-retrieved documents to generate responses directly without real-time
        retrieval.

        Returns:
            None: Indicates no implementation is provided.
        """
        pass

    def _load_no_source(self):
        """
        Placeholder method for the 'no_source' mode. This mode would generate responses without
        using any external document sources, relying solely on the language model's capabilities.

        Returns:
            None: Indicates no implementation is provided.
        """
        pass

    def invoke(self, question):
        """
        Invokes the RAG system with a given question and returns the generated answer. This method
        acts as the interface for external calls to the RAG system.

        Args:
            question (str): The query or question to be answered.

        Returns:
            Any: The output from the language model after processing the question.
        """
        return self.chain.invoke(question)
