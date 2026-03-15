''' Basic ETL DAG '''
from datetime import datetime, date
import pandas as pd
import os
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

# Shared directory path for all tasks
BASE_PATH = "/workspaces/hands-on-introduction-data-engineering-4395021/lab/end-to-end"
EXTRACT_FILE = f"{BASE_PATH}/basic-etl-extract-data.csv"
TRANSFORM_FILE = f"{BASE_PATH}/basic-etl-transform-data.csv"
DB_FILE = f"{BASE_PATH}/basic-etl-load-db.db"
DATA_URL = "https://datahub.io/core/top-level-domain-names/r/top-level-domain-names.csv.csv"

with DAG(
    dag_id='basic_etl_dag',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False
) as dag:

    # 1. EXTRACT: Use wget to download the CSV
    extract_task = BashOperator(
        task_id='extract_task',
        bash_command=f'mkdir -p {BASE_PATH} && wget -c -L {DATA_URL} -O {EXTRACT_FILE}'
    )

    # 2. TRANSFORM: Use Pandas to filter and add a date
    def transform_data():
        """Read in the file, and write a transformed file out"""
        today = date.today()
        
        df = pd.read_csv(EXTRACT_FILE)
        
        # Filtering for 'generic' type and adding the processing date
        generic_type_df = df[df['Type'] == 'generic'].copy()
        generic_type_df['Date'] = today.strftime('%Y-%m-%d')
        
        generic_type_df.to_csv(TRANSFORM_FILE, index=False)

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data
    )

    # 3. LOAD: Import the transformed CSV into a SQLite database
    load_task = BashOperator(
        task_id='load_task',
        bash_command=(
            f'echo -e ".separator \\",\\"\\n.import --skip 1 {TRANSFORM_FILE} top_level_domains" '
            f'| sqlite3 {DB_FILE}'
        )
    )

    # 4. Define the flow of the pipeline
    extract_task >> transform_task >> load_task