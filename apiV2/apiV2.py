from flask import Flask, Response
import requests
from datetime import datetime
import json

url = "https://api.openweathermap.org/data/2.5/onecall?lat=37.774929&lon=-122.419418&appid=31e8c0543689272d7d14e88ea2125892"

app = Flask(__name__)

def PeticionOpenWeather(intervalo):
    response = requests.get(url)
    dict = response.json()
    array = dict['hourly']

    predicciones = []
    hora = datetime.now().hour

    for index in range(len(array)):
        predicciones.append(
            {
                'hour': str(hora%24) + ":00",
                'temp': array[index]['temp'],
                'hum': array[index]['humidity']
            }
        )
        hora += 1
        if hora == intervalo:
            break 

    return predicciones

@app.route('/api/v2/24horas', methods=['GET'])
def api_predecir_24():
    predicciones = PeticionOpenWeather(24)
    res =  Response(json.dumps(predicciones), status = 200)
    res.headers['Content-Type']='application/json'
    return res

@app.route('/api/v2/48horas', methods=['GET'])
def api_predecir_48():
    predicciones = PeticionOpenWeather(48)
    res =  Response(json.dumps(predicciones), status = 200)
    res.headers['Content-Type']='application/json'
    return res

@app.route('/api/v2/72horas', methods=['GET'])
def api_predecir_72():
    predicciones = PeticionOpenWeather(72)
    res =  Response(json.dumps(predicciones), status = 200)
    res.headers['Content-Type']='application/json'
    return res
