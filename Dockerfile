FROM centos:latest

RUN yum install -y python mysql && curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && python get-pip.py

ADD hasker/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
