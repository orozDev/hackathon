FROM python:3.9-alpine3.16

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY . /app
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN adduser --disabled-password app-user
RUN chown -R app-user:app-user /app
RUN chmod -R 777 /app/static
RUN chmod -R 777 /app/media


RUN pip3 install -r requirements.txt

USER app-user