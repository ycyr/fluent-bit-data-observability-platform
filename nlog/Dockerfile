FROM python:3.8

ADD bin/nloggenerator.py /

RUN pip install rfc5424-logging-handler

CMD [ "python", "./nloggenerator.py" ]