FROM Python:3.6-alpine

ADD ./src /pyapp

WORKDIR /pyapp

RUN pip install -r requirements.txt

CMD python ./runserver.py