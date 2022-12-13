# syntax=docker/dockerfile:1
FROM tiangolo/uwsgi-nginx-flask:python3.11
WORKDIR /app
COPY ./app .
RUN rm main.py
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
EXPOSE 80