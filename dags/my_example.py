from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(days=1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'my_example', default_args=default_args)


start1 = KubernetesPodOperator(namespace='airflow',
                          image="python:3.6",
                          image_pull_policy="Always",
                          cmds=["python","-c"],
                          arguments=["print('hello world')"],
                          labels={"foo": "bar"},
                          name="start1",
                          resources={"request_cpu": "256m", "limit_cpu": "1", "request_memory": "256Mi","limit_memory": "1Gi"},
                          task_id="start1",
                          get_logs=True,
                          dag=dag
                          )

start2 = KubernetesPodOperator(namespace='airflow',
                          image="python:3.6",
                          image_pull_policy="Always",
                          cmds=["python","-c"],
                          arguments=["print('hello world')"],
                          labels={"foo": "bar"},
                          name="start2",
                          resources={"request_cpu": "256m", "limit_cpu": "1", "request_memory": "256Mi","limit_memory": "1Gi"},
                          task_id="start2",
                          get_logs=True,
                          dag=dag,
                          executor_config={
                              "KubernetesExecutor":
                              {
                                  "image": "apache/airflow:1.10.12-python3.8"
                              }
                          }

                          )
