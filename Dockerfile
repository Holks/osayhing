FROM python:3.6-alpine

RUN adduser -D registry

WORKDIR ~/registry

COPY requirements.txt requirements.txt
COPY create_shareholders.py create_shareholders.py 
COPY shareholders.txt shareholders.txt
COPY create_companies.py create_companies.py

RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN apk add -U --no-cache gcc build-base linux-headers ca-certificates  python3-dev libffi-dev libressl-dev libxslt-dev
RUN venv/bin/pip install --upgrade setuptools
RUN venv/bin/pip install  -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY osayhing.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP osayhing.py

RUN chown -R registry:registry ./
USER registry

EXPOSE 5000
ENTRYPOINT ["sh","./boot.sh"]
