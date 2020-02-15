FROM python:3

RUN mkdir /app/
ADD requirements.txt /tmp/
RUN cd /tmp && pip install -r requirements.txt

ADD ./ /app/

CMD python /app/owntracks_exporter.py
