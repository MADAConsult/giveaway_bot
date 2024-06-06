FROM python:3.10.4-slim-bullseye

COPY ./ ./


# Install dependencies
RUN pip install -r requirements.txt
