from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas

default_args = {
    'owner': 'Fernando Izquierdo',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'email': ['fer227@correo.ugr.es'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    #'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

# Inicialización del grafo DAG de tareas para el flujo de trabajo
dag = DAG(
    'predictor_sfrancisco',
    default_args=default_args,
    description='Predice la temperatura de San Francisco en las próximas horas',
    schedule_interval=timedelta(days=1),
)

def FormatearDatos():
    df_humedad = pandas.read_csv('/home/fer227/workdir/humidity.csv')
    df_temperatura = pandas.read_csv('/home/fer227/workdir/temperature.csv')
    df_formateado = pandas.DataFrame()

    col_humedad = df_humedad['San Francisco']
    col_temperatura = df_temperatura['San Francisco']
    col_fecha = df_humedad['datetime']

    df_formateado['DATE'] = col_fecha
    df_formateado['HUM'] = col_humedad
    df_formateado['TEMP'] = col_temperatura
    df_formateado.dropna(subset=['HUM'], inplace=True)
    df_formateado.dropna(subset=['TEMP'], inplace=True)

    df_formateado.to_csv('/home/fer227/workdir/datos.csv', index=False)


CrearDirectorio = BashOperator(
		task_id='CrearDirectorio',
		depends_on_past=False,
		bash_command='mkdir -p /home/fer227/workdir/',
		dag=dag
		)


ObtenerDatosHumedad = BashOperator(
		task_id='ObtenerDatosHumedad',
		depends_on_past=False,
		bash_command='curl -o /home/fer227/workdir/humidity.csv.zip  https://raw.githubusercontent.com/manuparra/MaterialCC2020/master/humidity.csv.zip',
		dag=dag
		)

ObtenerDatosTemperatura = BashOperator(
		task_id='ObtenerDatosTemperatura',
		depends_on_past=False,
		bash_command='curl -o /home/fer227/workdir/temperature.csv.zip https://raw.githubusercontent.com/manuparra/MaterialCC2020/master/temperature.csv.zip',
		dag=dag
		)

DescomprimirDatosHumedad = BashOperator(
		task_id='DescomprimirDatosHumedad',
		depends_on_past=True,
		bash_command='unzip -od /home/fer227/workdir/ /home/fer227/workdir/humidity.csv.zip',
		dag=dag
		)

DescomprimirDatosTemperatura = BashOperator(
		task_id='DescomprimirDatosTemperatura',
		depends_on_past=True,
   		bash_command='unzip -od /home/fer227/workdir/ /home/fer227/workdir/temperature.csv.zip',
   		dag=dag
		)

FormatearDatos = PythonOperator(
		task_id='FormatearDatos',
		depends_on_past=True,
		python_callable=FormatearDatos,
		dag=dag
		)

LanzarMongo = BashOperator(
    task_id='LanzarMongo',
    depends_on_past=True,
    bash_command="docker run -d -p 27017:27017 mongo:latest",
    dag=dag,
)

ImportarDatosMongo = BashOperator(
    task_id='ImportarDatosMongo',
    depends_on_past=True,
    bash_command="mongoimport --db predicciones --collection SanFrancisco --type csv --file /home/fer227/workdir/datos.csv --headerline --port 27017 --host localhost",
    dag=dag,
)

ClonarRepositorio = BashOperator(
    task_id='ClonarRepositorio',
    depends_on_past=True,
    bash_command="cd /home/fer227/workdir && git clone https://github.com/fer227/API_WeatherPredictor.git",
    dag=dag,
)

#EntrenarModelos = BashOperator(
#    task_id='EntrenarModelos',
#    depends_on_past=True,
#   bash_command="cd /home/fer227/workdir/API_WeatherPredictor/apiV1 && python arima.py",
#    dag=dag,
#)

DescomprimirModelos = BashOperator(
    task_id='DescomprimirModelos',
    depends_on_past=True,
    bash_command="cd /home/fer227/workdir/API_WeatherPredictor/apiV1 && unzip -od /home/fer227/workdir/API_WeatherPredictor/apiV1 /home/fer227/workdir/API_WeatherPredictor/apiV1/modelos.zip",
    dag=dag,
)

ConstruirImagenDockerV1 = BashOperator(
    task_id='ConstruirImagenDockerV1',
    depends_on_past=True,
    bash_command="cd /home/fer227/workdir/API_WeatherPredictor/apiV1 && docker build -t apiv1 .",
    dag=dag,
)

LanzarImagenDockerV1 = BashOperator(
    task_id='LanzarImagenDockerV1',
    depends_on_past=True,
    bash_command="cd /home/fer227/workdir/API_WeatherPredictor/apiV1 && docker run -d -p 6000:6000 -t apiv1",
    dag=dag,
)

ConstruirImagenDockerV2 = BashOperator(
    task_id='ConstruirImagenDockerV2',
    depends_on_past=True,
    bash_command="cd /home/fer227/workdir/API_WeatherPredictor/apiV2 && docker build -t apiv2 .",
    dag=dag,
)

LanzarImagenDockerV2 = BashOperator(
    task_id='LanzarImagenDockerV2',
    depends_on_past=True,
    bash_command="cd /home/fer227/workdir/API_WeatherPredictor/apiV2 && docker run -d -p 6001:6001 -t apiv2",
    dag=dag,
)

LanzarTestV1 = BashOperator(
    task_id='LanzarTestV1',
    depends_on_past=True,
    bash_command="cd /home/fer227/workdir/API_WeatherPredictor/apiV1 && python -m pytest test.py",
    dag=dag,
)

LanzarTestV2 = BashOperator(
    task_id='LanzarTestV2',
    depends_on_past=True,
    bash_command="cd /home/fer227/workdir/API_WeatherPredictor/apiV2 && python -m pytest test.py",
    dag=dag,
)


# Árbol de dependencias
CrearDirectorio >> [ObtenerDatosHumedad, ObtenerDatosTemperatura] 
ObtenerDatosHumedad >> [DescomprimirDatosHumedad, DescomprimirDatosTemperatura] 
ObtenerDatosTemperatura >> [DescomprimirDatosHumedad, DescomprimirDatosTemperatura]
DescomprimirDatosHumedad >> FormatearDatos >> LanzarMongo >> [ImportarDatosMongo, ClonarRepositorio] >> DescomprimirModelos >> [ConstruirImagenDockerV1, ConstruirImagenDockerV2]
DescomprimirDatosTemperatura >> FormatearDatos >> LanzarMongo >> [ImportarDatosMongo, ClonarRepositorio] >> DescomprimirModelos >> [ConstruirImagenDockerV1, ConstruirImagenDockerV2]
ConstruirImagenDockerV1 >> LanzarImagenDockerV1 >> LanzarTestV1
ConstruirImagenDockerV2 >> LanzarImagenDockerV2 >> LanzarTestV2