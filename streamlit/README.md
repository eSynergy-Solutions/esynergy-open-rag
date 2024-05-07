# Deployment

```bash
cd Streamlit

# Create .env file with the following secrets:
#MODEL_TYPE=bedrock
#LLM_MODEL=anthropic.claude-v2
#EMBEDDING_MODEL=amazon.titan-embed-text-v1
#STREAMLIT_URL=<streamlit-url>
#STREAMLIT_KEY=Basic <key>
#STREAMLIT_FEEDBACK_EMAIL=<feedback-email>
#STREAMLIT_FEEDBACK_PASSWORD=<feedback-password>
#STREAMLIT_PASSWORD=<steramlit-password>
#RETREIVER_NAME=astradb
#AWS_ACCESS_KEY_ID=<aws-access-key-id>
#AWS_SECRET_ACCESS_KEY=<aws-secret-access-key>
#ASTRA_DB_API_ENDPOINT=<astra-endpoint>
#ASTRA_DB_APPLICATION_TOKEN=<astra-token>
#ASTRA_DB_KEYSPACE=sandbox
#ASTRA_DB_COLLECTION=sandbox_sharepoint_docs
#PIP_GIT_USER=
#PIP_GIT_TOKEN=
#PIP_GIT_BRANCH=main

source .env

pip install -r requirements.txt
pip install git+https://${PIP_GIT_USER}:${PIP_GIT_TOKEN}@github.com/eSynergy-Solutions/OpenRag.git@${PIP_GIT_BRANCH}
streamlit run salesChat.py
```
