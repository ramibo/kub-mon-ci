FROM python:3.10.9-alpine3.17

RUN mkdir -p /app
WORKDIR /app

COPY ./src/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./src /app/

EXPOSE 5000
CMD ["python", "/app/server.py"]