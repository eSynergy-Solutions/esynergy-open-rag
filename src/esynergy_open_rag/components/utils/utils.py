import logging
import os


def check_env_variables(required_env_vars: list[str]) -> bool:
    """
    Check if required environment variables are set.

    Args:
        required_env_vars (list[str]): A list of required environment variable names.

    Returns:
        bool: True if all required environment variables are set, False otherwise.

    Raises:
        ValueError: If any required environment variables are missing.
    """
    missing_env_vars = [var for var in required_env_vars if not os.environ.get(var)]
    if missing_env_vars:
        logging.error(f"Missing required environment variables: {', '.join(missing_env_vars)}")
        raise ValueError(f"Missing required environment variables: {', '.join(missing_env_vars)}")

    return True
