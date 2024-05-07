FROM python:3.11-slim


WORKDIR /app

ARG PIP_USER
ARG PIP_PASS
ARG PIP_URL
ARG PIP_PORT

ENV PIP_FULL_URL=http://${PIP_USER}:${PIP_PASS}@${PIP_URL}:${PIP_PORT}

RUN pip install --index-url ${PIP_FULL_URL} --trusted-host ${PIP_URL} esynergy-open-rag==0.1.2

COPY *.py /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "salesChat.py"]
