Basic ETL Pipeline with Apache Airflow
📌 Project Overview
This project implements a classic ETL (Extract, Transform, Load) pipeline orchestrated by Apache Airflow. The workflow automates the process of fetching raw data regarding Top-Level Domains (TLDs), processing the data using Python/Pandas, and loading the final structured results into a SQLite database.

This project demonstrates proficiency in:

Workflow Orchestration: Managing task dependencies and scheduling.

Data Engineering: Automating the flow from raw source to queryable database.

Hybrid Operators: Combining BashOperator (for system-level tasks) and PythonOperator (for data manipulation).

🏗️ The Pipeline Architecture
The DAG (Directed Acyclic Graph) consists of three primary stages:
![Airflow DAG Graph](screenshots/airflow_graph.png)
1. Extract (extract_task)
Technology: BashOperator + wget

Action: Downloads a raw CSV file containing global TLD information from a remote data hub. It ensures the local directory exists before saving the file to prevent path errors.

2. Transform (transform_task)
Technology: PythonOperator + Pandas

Action: * Reads the raw CSV.

Filters the dataset to include only 'generic' domain types.

Injects a Date column representing the processing timestamp for data lineage.

Outputs a cleaned version to a secondary CSV.

3. Load (load_task)
Technology: BashOperator + SQLite3

Action: Utilizes a high-performance SQLite .import command to ingest the transformed CSV into a local database table named top_level_domains.

🛠️ Technical Stack
Language: Python 3.x

Orchestrator: Apache Airflow

Data Library: Pandas

Database: SQLite

Environment: Linux / VS Code Codespaces

🚀 Getting Started
Prerequisites
Airflow 2.x+ installed and configured.

Python libraries: pandas.

SQLite3 CLI installed on the host system.

Installation & Execution
Clone the repository to your Airflow dags/ folder:

Bash
cd ~/airflow/dags
git clone <your-repo-link>
Set the Base Path:
Update the BASE_PATH variable in the script to match your local environment's absolute path.

Initialize the Airflow DB:

Bash
airflow db init
Run the DAG:

Open the Airflow UI (usually at localhost:8080).

Unpause the basic_etl_dag.

Trigger the DAG manually.

📊 Verification
To verify the data has been loaded correctly into the database, run the following command in your terminal:

Bash
sqlite3 your_path/basic-etl-load-db.db "SELECT * FROM top_level_domains LIMIT 5;"
