FROM python:2.7

RUN apt-get update && apt-get install -y mysql-client libmysqlclient-dev

WORKDIR /opt/hasker

COPY ./requirements.txt /opt/hasker/requirements.txt

RUN pip install -r /opt/hasker/requirements.txt

COPY ./hasker/ /opt/hasker

ADD ./docker/entrypoint.sh /opt/hasker

EXPOSE 8000

RUN ["chmod", "+x", "./entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]