FROM python:3.6

EXPOSE 6001

COPY requirements.txt apiV2.py ./

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:6001 apiV2:app