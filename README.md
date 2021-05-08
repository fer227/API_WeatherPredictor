# API Weather Predictor
API para predecir el tiempo y la humedad en la ciudad de San Francisco durante un intervalo de tiempo. Cuenta con dos versiones:
- [apiV1](./apiV1). Cuenta con un predictor entrenado con *pmdarima*. 
- [apiV2](./apiV2). Coge las predicciones a su vez de la api de *openweathermap*.

Finalmente, en [dag_predictor_sfrancisco](./dag_predictor_sfracisco.py) podemos encontrar un *workflow* llevado a cabo con la herramienta **Apache Airflow** con las diferentes tareas para poder desplegarlo en cualquier máquina.