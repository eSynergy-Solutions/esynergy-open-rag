# create a class RAG that sets up a aRetreival AUgen,med chatbot with a given model and given retriever and sends backa chain as output

import logging
from typing import Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# from components.embeddings.embedding import Embedding
from esynergy_open_rag.components.llms.llm import LLM


class RAG:
    def __init__(self, llm: LLM, retriever, rag_type: Optional[str] = "with_source"):
        self.model = llm
        self.retriever = retriever
        self.rag_type = rag_type
        self.chain = self._load_chain()

    def _load_chain(self):
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
        pass

    def _load_no_source(self):
        pass

    def invoke(self, question):
        return self.chain.invoke(question)
