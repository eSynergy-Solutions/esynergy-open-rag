import os.path

from pydantic import BaseSettings


# these settings are loaded from three sources:
# 1. defaults in the source code (lowest precedence)
# 2. environment variables (highest precedence)
class TestConfig(BaseSettings):
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "config.env")


CONFIG = TestConfig()
