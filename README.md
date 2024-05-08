# esynergy Open RAG

<p align="center">
    <img src="./assets/logo.png" width="30%">
</p>

#

## Architecture Overview

**esynergy Open RAG** is a versatile framework designed to streamline the creation of RAG-based AI applications. By abstracting the complexities involved in setting up various components, it offers a simplified approach to developing sophisticated AI solutions. The framework allows developers to configure essential elements through environment variables, enabling rapid deployment and customization of Retrieve-Augment-Generate (RAG) systems. Here are the key components supported by the **esynergy Open RAG** framework:

- **Document Loaders**: These components facilitate the efficient ingestion and processing of vector data, ensuring that data from various sources can be easily integrated and utilized within the RAG environment.
- **Embeddings**: This module allows for the dynamic loading of different types of embeddings based solely on configuration settings defined in the environment variables. This flexibility supports a wide range of use cases and optimizations.
- **LLMs (Large Language Models)**: It provides mechanisms to load and deploy various language models according to the specific needs dictated by the environment settings. This adaptability ensures that the most appropriate computational resources are used for each task.
- **RAGs (Retrieve-Augment-Generate Systems)**: The framework supports multiple types of RAG configurations such as with_source, from_docs, or no_source, enabling developers to tailor the information retrieval and generation process to the specific demands of the application.
- **Retrievers**: Integrating seamlessly with popular databases and search engines such as Astra DB, Supabase, Elasticsearch, and OpenSearch, this module loads retriever objects that are crucial for efficient data retrieval in RAG systems.
- **Streamlit Components**: Dedicated components designed to facilitate the integration with the Streamlit platform, allowing for the swift development of user-friendly AI assistants and interactive elements within the application.

By providing these configurable modules, **esynergy Open RAG** empowers developers to build robust AI-driven applications with ease, focusing on innovation and customization without the burden of extensive setup processes.

## Project Structure

Below is the project structure for **esynergy Open RAG**, providing an overview of the main components:

```
├── .github/                   # GitHub related files like workflows and actions
│ └── workflows/               # CI/CD pipeline scripts
├── assets/                    # Media assets such as logos
├── docs/                      # Documentation for the project
├── scripts/                   # Maintenance and setup scripts
├── src/                       # Contains all source code
│ └── esynergy_open_rag/       # Main application package
├── tests/                     # Automated tests
├── .flake8                    # Flake8 configuration file
├── .gitignore                 # Specifies intentionally untracked files to ignore
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── CHANGELOG.md               # Project changelog
├── CODING-CONVENTIONS.md      # Coding standards and conventions
├── comments.md                # Project comments and notes
├── CONTRIBUTING.md            # Guidelines for contributing to the project
├── LICENSE.txt                # The license under which the project is made available
├── poetry.lock                # Poetry lock file for dependencies management
├── pyproject.toml             # Poetry configuration file
├── README.md                  # Project overview and setup instructions
├── requirements.txt           # Python package dependencies
└── setup.py                   # Setup script for the project
```

## Architecture Overview

The **esynergy Open RAG** application employs a Retrieve-Augment Chatbot architecture, incorporating:

- **Document Loaders**: Facilitate the ingestion and processing of vector data.
- **Embeddings**: Enable loading various types of embeddings through configurations set in the environment variables.
- **LLMs (Large Language Models)**: Allow the loading of different types of language models based on the provided model type and name.
- **RAGs (Retrieve-Augment-Generate Systems)**: Support the loading of different RAG types, such as with_source, from_docs, or no_source.
- **Retrievers**: Load retriever objects for databases and search engines like Astra DB, Supabase, Elasticsearch, and OpenSearch.
- **Streamlit Components**: Simplify integration with Streamlit to build AI assistants efficiently.


## Install
```bash
pip install git+https://${PIP_GIT_USER}:${PIP_GIT_TOKEN}@github.com/eSynergy-Solutions/esynergy-open-rag.git@${PIP_GIT_BRANCH}
```

## Usage
```bash
# Create .env file with the following secrets (Some configs may not be required):
# MODEL_TYPE=
# LLM_MODEL=
# EMBEDDING_MODEL=
#
# RETRIEVER_NAME=
#
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
#
# ASTRA_DB_API_ENDPOINT=
# ASTRA_DB_APPLICATION_TOKEN=
# ASTRA_DB_KEYSPACE=
# ASTRA_DB_COLLECTION=
```
```python
import logging
from esynergy_open_rag.config import chain

response = chain.invoke("summary of the datamesh project")
logging.info(response)
```

## Test
```bash
# Create .env file with the following secrets (Some configs may not be required):
# MODEL_TYPE=
# LLM_MODEL=
# EMBEDDING_MODEL=
#
# RETRIEVER_NAME=
#
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
#
# ASTRA_DB_API_ENDPOINT=
# ASTRA_DB_APPLICATION_TOKEN=
# ASTRA_DB_KEYSPACE=
# ASTRA_DB_COLLECTION=

poetry install
bash scripts/build_and_test.sh
```

## Generate Docs
```bash
# Auto generate docs
poetry run sphinx-apidoc -o docs_generation src -f

cd docs_generation
make html

# Replace html folder
cd ..
rm -rf docs/*
cp -r docs_generation/_build/html/* ./docs/
# Fixing style bug
touch .nojekyll
```


## 📑 License
esynergy Open RAG is distributed under the MIT License. See [LICENSE.md](https://github.com/robusta-dev/robusta/blob/master/LICENSE) for more information.
