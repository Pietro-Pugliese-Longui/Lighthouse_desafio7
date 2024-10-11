from airflow.utils.edgemodifier import Label
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.models import Variable
import sqlite3
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def export_orders():
    conn = sqlite3.connect('/opt/airflow/data/Northwind_small.sqlite')
    orders = pd.read_sql_query("SELECT * FROM [Order]", conn)  
    orders.to_csv('/opt/airflow/data/output_orders.csv', index=False)  
    conn.close()

def count_rio_orders():
    conn = sqlite3.connect('/opt/airflow/data/Northwind_small.sqlite')
    orders = pd.read_csv('/opt/airflow/data/output_orders.csv')  
    order_details = pd.read_sql_query("SELECT * FROM [OrderDetail]", conn)
    
    merged_data = pd.merge(orders, order_details, left_on='Id', right_on='OrderId')
    rio_orders = merged_data[merged_data['ShipCity'] == 'Rio de Janeiro']
    total_quantity = rio_orders['Quantity'].sum()
    
    with open('/opt/airflow/data/count.txt', 'w') as f:  
        f.write(str(total_quantity))
    
    conn.close()    

def export_final_answer():
    import base64

    with open('/opt/airflow/data/count.txt') as f:  
        count = f.readlines()[0]

    my_email = Variable.get("my_email")
    message = my_email + count
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    with open("/opt/airflow/data/final_output.txt", "w") as f:  
        f.write(base64_message)

    return None

with DAG(
    'DesafioAirflow',
    default_args=default_args,
    description='Desafio de Airflow da Indicium',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    dag.doc_md = """
        Esse é o desafio de Airflow da Indicium.
    """

    export_orders_task = PythonOperator(
        task_id='export_orders',
        python_callable=export_orders,
    )

    count_rio_orders_task = PythonOperator(
        task_id='count_rio_orders',
        python_callable=count_rio_orders,
    )

    export_final_output = PythonOperator(
        task_id='export_final_output',
        python_callable=export_final_answer,
        provide_context=True
    )

    export_orders_task >> count_rio_orders_task >> export_final_output
