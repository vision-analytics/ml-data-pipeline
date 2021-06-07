FROM python:3.6

ENV PYTHONPATH /app
ENV CELERY_BROKER redis://redis:6379/0
ENV CELERY_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

RUN mkdir app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


COPY . /app

RUN mkdir -p output logs

#ENTRYPOINT celery celery.tasks --app=:app --loglevel=info
#ENTRYPOINT celery -A tasks worker --loglevel=info