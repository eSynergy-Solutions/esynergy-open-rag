import os

from dotenv import load_dotenv

from esynergy_open_rag.components.llms.llm import LLM

load_dotenv()


class TestLlm:
    def test_llm(self):
        model_name = os.getenv("LLM_MODEL")
        llm = LLM(model_type="bedrock", model_name=model_name)
        result = llm.llm("Hello World")
        assert result != "" or result is not None
