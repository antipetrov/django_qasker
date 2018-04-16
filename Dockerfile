FROM jfloff/alpine-python:2.7-slim

RUN apk add python python-devel python-pip

WORKDIR /opt/hasker

COPY requirements.txt /opt/hasker/requirements.txt


RUN pip install -r /opt/hasker/requirements.txt

COPY ./ /opt/hasker

EXPOSE 8000

CMD ["uwsgi", "--ini", "/opt/hasker/uwsgi.ini"]