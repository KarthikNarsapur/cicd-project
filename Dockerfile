FROM python:3.8-alpine

ADD ./src/requirements.txt /pyapp/requirements.txt

WORKDIR /pyapp

RUN pip install -r requirements.txt

ADD ./src /pyapp

CMD python ./runserver.py