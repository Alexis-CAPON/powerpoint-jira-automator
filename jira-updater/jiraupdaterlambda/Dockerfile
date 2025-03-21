FROM python:3.11-slim-buster

COPY requirements.txt ./
COPY app.py jira_updater.py openai_call.py ppt_extractor.py ./

RUN apt-get update && apt-get install -y libreoffice poppler-utils && rm -rf /var/lib/apt/lists/*
RUN python3.11 -m pip install -r requirements.txt -t .
RUN python3.11 -m pip install awslambdaric

CMD ["python3.11", "-m", "awslambdaric", "app.lambda_handler"]