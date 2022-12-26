FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3

RUN apt-get -y install python3-pip

COPY ./ .
RUN . /env/bin/activate && pip install -r /req.txt

ENV FLASK_APP=/main.py

CMD . /venv/bin/activate
