# syntax=docker/dockerfile:1
FROM tiangolo/uwsgi-nginx-flask:python3.8
WORKDIR /app
COPY ./app .
EXPOSE 80
RUN pip3 install -r requirements.txt