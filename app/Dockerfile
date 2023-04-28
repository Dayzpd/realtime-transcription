FROM python:3.10-slim-bullseye

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y ffmpeg

ENV PYTHONPATH=/app

WORKDIR ${PYTHONPATH}

RUN pip install --upgrade pip setuptools wheel

COPY ./requirements.txt .

RUN python -m pip install --no-cache-dir -r ./requirements.txt

RUN mkdir data
RUN mkdir transcription

#COPY ./main.py .