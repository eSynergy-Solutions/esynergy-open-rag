import os
from typing import Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, WebBaseLoader
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain_community.vectorstores import FAISS


class VectorIngestor:
    """
    Class for ingesting and processing vector data.

    Args:
        embeddings (str): The type of embeddings to use.
        vector_store_type (str): The type of vector store to use.
        index_path (str, optional): The path to save the index file. Defaults to "faiss.index".
        source_type (str, optional): The type of data source. Defaults to "directory".
        source (str, optional): The source of the data. Defaults to "uploaded_pdfs".

    Attributes:
        embeddings (str): The type of embeddings being used.
        vector_store_type (str): The type of vector store being used.
        index_path (str): The path to the index file.
        vector_store (object): The vector store object.
        source (str): The source of the data.
        source_type (str): The type of data source.
        docs (list): The loaded documents.
    """

    def __init__(
        self,
        embeddings: str,
        vector_store_type: str,
        index_path: Optional[str] = "faiss.index",
        source_type: Optional[str] = "directory",
        source: Optional[str] = "uploaded_pdfs",
    ):
        """
        Initialize a VectorIngestor instance.

        Args:
            embeddings (str): The type of embeddings to use.
            vector_store_type (str): The type of vector store to use.
            index_path (str, optional): The path to save the index file. Defaults to "faiss.index".
            source_type (str, optional): The type of data source. Defaults to "directory".
            source (str, optional): The source of the data. Defaults to "uploaded_pdfs".
        """
        self.embeddings = embeddings
        self.vector_store_type = vector_store_type
        self.index_path = index_path
        self.vector_store = None
        self.source = source
        self.source_type = source_type
        self.docs = self._load_from_source()

    def _load_from_source(self) -> list:
        """
        Load documents from the specified source.

        Returns:
            list: The loaded documents.
        """
        if self.source_type == "directory":
            loader = DirectoryLoader(self.source, glob="**/*.pdf")
            docs = loader.load()
            return docs
        elif self.source_type == "sitemap":
            # langchain sitemap loader
            sitemap_loader = SitemapLoader(web_path=self.source)
            docs = sitemap_loader.load()
            return docs
        elif self.source_type == "websites":
            # langchain website loader
            website_loader = WebBaseLoader(self.source)
            docs = website_loader.load()
            return docs

    def document_splitter(self) -> list:
        """
        Split the loaded documents into smaller chunks.

        Returns:
            list: The split texts.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )
        docs = self._load_from_source()
        texts = text_splitter.split_documents(docs)
        return texts

    def ingest_documents(self):
        """
        Ingest the documents into the vector store.
        """
        texts = self.document_splitter()
        if self.vector_store_type == "FAISS":
            vector_store = FAISS.from_documents(texts, self.embeddings)
            # append to the existing index
            # check if self.index_path exists on the disk if so load it
            if os.path.exists(self.index_path):
                self.load_vector_store()
                self.vector_store.merge_from(vector_store)
            else:
                self.vector_store = vector_store
            self.vector_store.save_local(self.index_path)
        # Add more vector store types here if needed

    def load_vector_store(self):
        """
        Load the vector store from the index file.
        """
        if self.vector_store_type == "FAISS":
            self.vector_store = FAISS.load_local(self.index_path, self.embeddings)
        # Add more vector store types here if needed

    def search_similar_documents(self, query: str, k: int = 5) -> list:
        """
        Search for similar documents based on the given query.

        Args:
            query (str): The query text.
            k (int, optional): The number of similar documents to retrieve. Defaults to 5.

        Returns:
            list: The similar documents.

        Raises:
            ValueError: If the vector store is not loaded.
        """
        if self.vector_store is None:
            raise ValueError("Vector store not loaded")

        results = self.vector_store.similarity_search(query, k=k)
        return results
