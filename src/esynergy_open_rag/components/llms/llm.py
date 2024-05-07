import logging
import os

import boto3
from dotenv import load_dotenv
from langchain_community.llms.bedrock import Bedrock
from langchain_google_genai import GoogleGenerativeAI

from esynergy_open_rag.components.utils.utils import check_env_variables

load_dotenv()


class LLM:
    """
    Class for loading different types of Language Model (LLM) based on the provided model type and name.

    Args:
        model_type (str): The type of the language model (e.g., "llamacpp", "gpt4all", "openai", "fireworks", "google", "bedrock").
        model_name (str): The name of the model.

    Attributes:
        model_type (str): The type of the language model.
        model_name (str): The name of the model.
        llm: The loaded language model object based on the provided model type and name.

    Raises:
        ValueError: If the provided model type is not supported.
        KeyError: If required environment variables are not set (for certain model types).
    """

    def __init__(self, model_type: str, model_name: str):
        """
        Initialize an LLM instance.

        Args:
            model_type (str): The type of the language model (e.g., "llamacpp", "gpt4all", "openai", "fireworks", "google", "bedrock").
            model_name (str): The name of the model.

        Raises:
            ValueError: If the provided model type is not supported.
            KeyError: If required environment variables are not set (for certain model types).
        """
        self.model_type = model_type
        self.model_name = model_name
        self.llm = self._load_llm()

    def _load_llm(self):
        """
        Load the language model based on the provided model type.

        Returns:
            The loaded language model object.

        Raises:
            ValueError: If the provided model type is not supported.
            KeyError: If required environment variables are not set (for certain model types).
        """
        if self.model_type == "llamacpp":
            logging.info(f"Loading LLM {self.model_type}")
            return self._load_llamacpp()
        elif self.model_type == "gpt4all":
            logging.info(f"Loading LLM {self.model_type}")
            return self._load_gpt4all()
        elif self.model_type == "openai":
            logging.info(f"Loading LLM {self.model_type}")
            return self._load_openai()
        elif self.model_type == "fireworks":
            logging.info(f"Loading LLM {self.model_type}")
            return self._load_fireworks()
        elif self.model_type == "google":
            logging.info(f"Loading LLM {self.model_type}")
            print("Google Model Loaded")
            return self._load_google()
        elif self.model_type == "bedrock":
            logging.info(f"Loading LLM {self.model_type}")
            return self._load_bedrock()
        else:
            logging.info(f"Tried loading LLM {self.model_type}, not supported.")
            raise ValueError("Model type not supported")

    def _load_bedrock(self):
        """
        Load Bedrock language model.

        Returns:
            Bedrock language model.

        Raises:
            KeyError: If required environment variables are not set.
        """
        required_env_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
        check_env_variables(required_env_vars)

        region = os.environ.get("AWS_REGION", "us-east-1")

        bedrock = boto3.client("bedrock-runtime", region_name=region)
        llm = Bedrock(model_id=self.model_name, client=bedrock)
        return llm

    def _load_llamacpp(self):
        """
        Load Llamacpp language model.

        Not implemented yet.
        """
        pass

    def _load_google(self):
        """
        Load Google language model.

        Returns:
            Google language model.
        """
        required_env_vars = ["GOOGLE_API_KEY"]
        check_env_variables(required_env_vars)

        self.model_name = os.environ.get("GOOGLE_MODEL_NAME", "gemini-pro")

        google_api_key = os.getenv("GOOGLE_API_KEY")
        llm = GoogleGenerativeAI(
            model=self.model_name,
            google_api_key=google_api_key,
            max_output_tokens=2048,
            max_retries=20,
            temperature=0.9,
        )
        return llm

    def _load_gpt4all(self):
        """
        Load GPT4All language model.

        Not implemented yet.
        """
        pass

    def _load_openai(self):
        """
        Load OpenAI language model.

        Not implemented yet.
        """
        pass

    def _load_fireworks(self):
        """
        Load Fireworks language model.

        Not implemented yet.
        """
        pass
