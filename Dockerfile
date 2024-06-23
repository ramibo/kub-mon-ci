FROM python:3.10.9-slim-buster

RUN mkdir -p /app
RUN apt-get update -y && apt-get install -y gcc
WORKDIR /app

COPY ./src/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./src /app/

EXPOSE 5000
CMD ["python", "/app/server.py"]
