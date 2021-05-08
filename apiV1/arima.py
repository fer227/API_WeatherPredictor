import pmdarima
import pandas
import pymongo
import pickle

def entrenar():
    client = pymongo.MongoClient("mongodb://0.0.0.0:27017")
    db = client["predicciones"]
    coleccion = db["SanFrancisco"]
    df = pandas.DataFrame(list(coleccion.find()))

    modelo_temperatura = pmdarima.auto_arima(
        df['TEMP'],
        start_p=1, start_q=1,
        test='adf',       # use adftest to find optimal 'd'
        max_p=3, max_q=3, # maximum p and q
        m=1,              # frequency of series
        d=None,           # let model determine 'd'
        seasonal=False,   # No Seasonality
        start_P=0,
        D=0,
        trace=True,
        error_action='ignore',
        suppress_warnings=True,
        stepwise=True)

    pickle.dump(modelo_temperatura, open("./modelo_temperatura.p", "wb" ) )

    modelo_humedad = pmdarima.auto_arima(
        df['HUM'],
        start_p=1, start_q=1,
        test='adf',       # use adftest to find optimal 'd'
        max_p=3, max_q=3, # maximum p and q
        m=1,              # frequency of series
        d=None,           # let model determine 'd'
        seasonal=False,   # No Seasonality
        start_P=0,
        D=0,
        trace=True,
        error_action='ignore',
        suppress_warnings=True,
        stepwise=True)
        
    pickle.dump(modelo_humedad, open("./modelo_humedad.p", "wb" ) )

if __name__ == "__main__":
    entrenar()