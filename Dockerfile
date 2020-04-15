FROM python:3.7-alpine

WORKDIR /app

RUN apk add --no-cache jq

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY processing/*.py /app/processing/
COPY *.py /app/
COPY run.sh /app/
RUN chmod +x /app/run.sh
RUN mkdir /app/data

ENTRYPOINT [ "ash", "/app/run.sh" ]