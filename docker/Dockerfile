FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y \
    curl apt-utils apt-transport-https debconf-utils gcc build-essential g++ git\
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./docker/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./docker/start-celeryworker /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app
EXPOSE 80
EXPOSE 8888
