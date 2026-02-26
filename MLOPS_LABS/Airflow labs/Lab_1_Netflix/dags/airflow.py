from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from src.lab import (
    load_data, 
    data_preprocessing, 
    build_save_model, 
    load_model_elbow,
    create_elbow_visualization,  # NEW
    analyze_clusters             # NEW
)

default_args = {
    "owner": "harini",
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="Airflow_Lab1_Enhanced",
    default_args=default_args,
    description="Enhanced Netflix clustering pipeline with visualization and analysis",
    start_date=datetime(2026, 2, 10),
    schedule_interval=None,
    catchup=False,
    tags=["lab1", "netflix", "clustering", "enhanced"],
) as dag:

    # Task 1: Load data
    t1 = PythonOperator(
        task_id="load_data_task",
        python_callable=load_data,
    )

    # Task 2: Preprocess data
    t2 = PythonOperator(
        task_id="data_preprocessing_task",
        python_callable=data_preprocessing,
        op_args=[t1.output],
    )

    # Task 3: Build and save model
    t3 = PythonOperator(
        task_id="build_save_model_task",
        python_callable=build_save_model,
        op_args=[t2.output, "kmeans_netflix.pkl"],
    )

    # Task 4: Load and verify model
    t4 = PythonOperator(
        task_id="load_model_task",
        python_callable=load_model_elbow,
        op_args=["kmeans_netflix.pkl", t3.output],
    )

    # Task 5: Create visualization (NEW)
    t5 = PythonOperator(
        task_id="create_visualization_task",
        python_callable=create_elbow_visualization,
        op_args=[t3.output],
    )

    # Task 6: Analyze clusters (NEW)
    t6 = PythonOperator(
        task_id="analyze_clusters_task",
        python_callable=analyze_clusters,
        op_args=["kmeans_netflix.pkl"],
    )

    # Dependencies: t4, t5, t6 run in parallel after t3
    t1 >> t2 >> t3 >> [t4, t5, t6]