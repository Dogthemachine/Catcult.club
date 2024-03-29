# Dockerfile
FROM python:3.8
ENV PYTHONUNBUFFERED 1
EXPOSE 8080
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip
RUN apt update
RUN apt install gettext -y
RUN pip install -r requirements.txt