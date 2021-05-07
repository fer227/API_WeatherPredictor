from flask import Flask, Response
import json
import pickle
import pmdarima
from datetime import datetime
import pandas as pd

def predecir(period):
    pred_temp = pickle.load( open('./modelo_temperatura.p', 'rb') )
    pred_hum = pickle.load( open('./modelo_humedad.p', 'rb') )

    prediccion_temp = pred_temp.predict(n_periods=period)
    prediccion_hum = pred_hum.predict(n_periods=period)

    predicciones = []
    hora = datetime.now().hour

    for tiempo, humedad in zip(prediccion_temp, prediccion_hum):
        predicciones.append(
            {
                'hour': str(hora%24) + ":00",
                'temp': tiempo,
                'hum': humedad
            }
        )

        hora += 1 

    return predicciones

app = Flask(__name__)

@app.route('/api/v1/24horas', methods=['GET'])
def api_predecir_24():
    res =  Response(json.dumps(predecir(24)), status = 200)
    res.headers['Content-Type']='application/json'
    return res

@app.route('/api/v1/48horas', methods=['GET'])
def api_predecir_48():
    res =  Response(json.dumps(predecir(48)), status = 200)
    res.headers['Content-Type']='application/json'
    return res

@app.route('/api/v1/72horas', methods=['GET'])
def api_predecir_72():
    res =  Response(json.dumps(predecir(72)), status = 200)
    res.headers['Content-Type']='application/json'
    return res