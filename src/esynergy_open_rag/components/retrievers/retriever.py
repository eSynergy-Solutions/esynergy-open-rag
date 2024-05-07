"""
This module contains the configuration and setup for the retrievers used in the OrgChat application.
It includes functions to create retriever objects for Supabase, Elasticsearch, and OpenSearch.
"""

import logging
import os
from pathlib import Path

import boto3
from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_astradb import AstraDBVectorStore
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_core.output_parsers import BaseOutputParser
from opensearchpy import RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from esynergy_open_rag.components.llms.llm import LLM

load_dotenv()

src: str = f"{Path(__file__).resolve().parents[2]}"
os.sys.path.append(src)


class LineListOutputParser(BaseOutputParser[list[str]]):
    """Output parser for a list of lines."""

    def parse(self, text: str) -> list[str]:
        """
        Parses the given text and returns a LineList object.

        Args:
            text (str): The text to be parsed.

        Returns:
            LineList: The parsed LineList object.
        """
        logging.debug(f"parsing text: {text} \n")
        lines = text.strip().split("\n")
        lines = [
            line for line in lines if line.strip() and "alternative" not in line and "original question" not in line
        ]
        return lines


class Retriever:
    def __init__(self):
        llm = LLM(model_type=os.getenv("MODEL_TYPE"), model_name=os.getenv("LLM_MODEL")).llm

        output_parser = LineListOutputParser()

        QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI language model assistant for the consulting company esynergy who have various clients. Your task is to generate one
            different versions of the given user question to retrieve relevant documents from a vector
            database. By generating one different perspectives on the user question, your goal is to help
            the user overcome some of the limitations of the distance-based similarity search.
            Provide these alternative one questions separated by newlines. also do not change the context of the questions and do not generate more number of questions. Also include the original question also as the first question.
            Original question: {question}""",
        )

        self.llm_chain = LLMChain(llm=llm, prompt=QUERY_PROMPT, output_parser=output_parser)

    def get_retriever(self, retriever_name, embeddings):
        """
        Returns a retriever object based on the specified retriever name.

        Args:
            retriever_name (str): The name of the retriever.
            embeddings: The embeddings to be used for retrieval.

        Returns:
            The retriever object.
        """
        if retriever_name == "supabase":
            return self.get_supabase_retriever(embeddings)
        elif retriever_name == "elasticsearch":
            return self.get_elastic_retriever(embeddings)
        elif retriever_name == "opensearch":
            return self.get_opensearch_retriever(embeddings)
        elif retriever_name == "astradb":
            return self.get_astradb_retriever(embeddings)
        else:
            raise ValueError(f"Invalid retriever name: {retriever_name}")

    @staticmethod
    def get_supabase_retriever(embeddings):
        pass

    @staticmethod
    def get_elastic_retriever(embeddings):
        pass

    def get_astradb_retriever(
        self,
        embeddings,
        llm_chain: LLMChain = None,
    ):
        if not llm_chain:
            llm_chain = self.llm_chain

        collection_name = os.getenv("ASTRA_DB_COLLECTION")
        namespace = os.getenv("ASTRA_DB_KEYSPACE")
        astra_url = os.getenv("ASTRA_DB_API_ENDPOINT")

        vstore = AstraDBVectorStore(
            embedding=embeddings,
            collection_name=collection_name,
            token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
            api_endpoint=astra_url,
            namespace=namespace,
        )

        retriever = vstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})

        retriever_from_llm = MultiQueryRetriever(
            retriever=retriever,
            llm_chain=llm_chain,
            parser_key="lines",
            include_original=True,
        )
        # make a parser for the output to remove empty lines
        return retriever_from_llm

    def get_opensearch_retriever(
        self,
        embeddings,
        llm_chain: LLMChain = None,
    ):
        """
        Returns an OpenSearch retriever object configured with the specified parameters.

        Parameters:
        - embeddings: The embedding function used for vector search.
        - index_name: The name of the index to search in OpenSearch. Default is "sharepoint_s3_bid_index2".
        - opensearch_url: The URL of the OpenSearch endpoint. Default is "https://bfkxqtzf33xbb7sb6jcl.us-east-1.aoss.amazonaws.com".

        Returns:
        - retriever_from_llm: The configured OpenSearch retriever object.
        """
        if not llm_chain:
            llm_chain = self.llm_chain

        index_name = os.getenv("OPENSEARCH_INDEX_NAME")
        opensearch_url = os.getenv("OPENSEARCH_URL")

        credentials = boto3.Session().get_credentials()
        region = "us-east-1"
        service = "aoss"
        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            region,
            service,
            session_token=credentials.token,
        )

        vector_store = OpenSearchVectorSearch(
            embedding_function=embeddings,
            index_name=index_name,
            opensearch_url=opensearch_url,
            http_auth=awsauth,
            timeout=300,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )

        retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 5})

        retriever_from_llm = MultiQueryRetriever(
            retriever=retriever,
            llm_chain=llm_chain,
            parser_key="lines",
            include_original=True,
        )
        # make a parser for the output to remove empty lines
        return retriever_from_llm
