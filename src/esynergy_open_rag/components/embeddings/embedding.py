import logging

import boto3
from dotenv import load_dotenv
from langchain_community.embeddings import (
    BedrockEmbeddings,
    GPT4AllEmbeddings,
    HuggingFaceInstructEmbeddings,
)

from esynergy_open_rag.components.utils.utils import check_env_variables

load_dotenv()


class Embedding:
    """
    Class for loading different types of embeddings based on the provided model type and name.

    Args:
        model_type (str): The type of the model (e.g., "llamacpp", "gpt4all", "openai", "fireworks", "huggingface-instruct").
        model_name (str): The name of the model.

    Attributes:
        model_type (str): The type of the model.
        model_name (str): The name of the model.
        embedding: The loaded embedding object based on the provided model type and name.

    Raises:
        ValueError: If the provided model type is not supported.
        KeyError: If required environment variables are not set (for certain model types).
    """

    def __init__(
        self,
        model_type: str,
        model_name: str,
    ):
        """
        Initialize an Embedding instance.

        Args:
            model_type (str): The type of the model (e.g., "llamacpp", "gpt4all", "openai", "fireworks", "huggingface-instruct").
            model_name (str): The name of the model.

        Raises:
            ValueError: If the provided model type is not supported.
            KeyError: If required environment variables are not set (for certain model types).
        """
        self.model_type = model_type
        self.model_name = model_name
        self.embedding = self._load_embedding()

    def _load_embedding(self):
        """
        Load the embedding based on the provided model type.

        Returns:
            The loaded embedding object.

        Raises:
            ValueError: If the provided model type is not supported.
            KeyError: If required environment variables are not set (for certain model types).
        """
        if self.model_type == "llamacpp":
            logging.info(f"Loading embedding {self.model_type}")
            return self._load_llamacpp()
        elif self.model_type == "gpt4all":
            logging.info(f"Loading embedding {self.model_type}")
            return self._load_gpt4all()
        elif self.model_type == "openai":
            logging.info(f"Loading embedding {self.model_type}")
            return self._load_openai()
        elif self.model_type == "fireworks":
            logging.info(f"Loading embedding {self.model_type}")
            return self._load_fireworks()
        elif self.model_type == "huggingface-instruct":
            logging.info(f"Loading embedding {self.model_type}")
            return self._load_huggingface_instruct()
        elif self.model_type == "bedrock":
            logging.info(f"Loading embedding {self.model_type}")
            return self._load_bedrock()
        else:
            logging.info(f"Tried loading embedding {self.model_type} not supported.")
            raise ValueError("Model type not supported")

    def _load_bedrock(self):
        """
        Load Bedrock embeddings.

        Returns:
            Bedrock embeddings.

        Raises:
            KeyError: If required environment variables are not set.
        """
        required_env_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
        check_env_variables(required_env_vars)
        bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
        embeddings = BedrockEmbeddings(client=bedrock, model_id=self.model_name)
        return embeddings

    def _load_huggingface_instruct(self):
        """
        Load Hugging Face Instruct embeddings.

        Returns:
            Hugging Face Instruct embeddings.
        """
        embeddings = HuggingFaceInstructEmbeddings(query_instruction="Represent the query for retrieval: ")
        return embeddings

    def _load_llamacpp(self):
        """
        Load Llamacpp embeddings.

        Not implemented yet.
        """
        pass

    def _load_gpt4all(self):
        """
        Load GPT4All embeddings.

        Returns:
            GPT4All embeddings.
        """
        embeddings = GPT4AllEmbeddings()
        return embeddings

    def _load_openai(self):
        """
        Load OpenAI embeddings.

        Not implemented yet.
        """
        pass

    def _load_fireworks(self):
        """
        Load Fireworks embeddings.

        Not implemented yet.
        """
        pass
