FROM python:3

RUN mkdir /app/
ADD requirements.txt /tmp/
RUN cd /tmp && pip install -r requirements.txt

ENV OT_POLLING_DELAY 60
ENV PROMETHEUS_PORT 60

ADD ./ /app/

CMD python /app/owntracks_exporter.py
