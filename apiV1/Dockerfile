FROM python:3.6

EXPOSE 6000

COPY requirements.txt apiV1.py arima.py modelo_humedad.p modelo_temperatura.p ./

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:6000 apiV1:app