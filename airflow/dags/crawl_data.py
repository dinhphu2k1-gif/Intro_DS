# datetime
from datetime import timedelta, datetime

# The DAG object
from airflow import DAG

# Operators
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.hooks.ssh_hook import SSHHook

# add a new SSH connection using the WEB UI under the admin --> connections tab.
sshHook = SSHHook("ssh-local")

# initializing the default arguments
default_args = {
    'owner': 'phukaioh',
    'start_date': datetime(2022, 3, 4),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}


# Instantiate a DAG object
crawl_dag = DAG('crawl_data',
                default_args=default_args,
                description='crawl data',
                schedule_interval='5 * * * *',
                catchup=False,
                tags=['dinhphu']
                )

start_task = DummyOperator(task_id='start_task', dag=crawl_dag)

run_command = "cd /opt/project/ && ls -la && pip install scrapy && bash run_crawl_vietnamnet.sh "
run_opetator = BashOperator(
    task_id="crawler",
    bash_command=run_command,
    dag=crawl_dag
)

now = datetime.now()  # current date and time
date = now.strftime("%d-%m-%Y")
file_name = "/data/vietnamnet/vietnamnet-" + date + ".json"
copy_command = "/opt/hadoop/bin/hdfs dfs -copyFromLocal -f /home/phukaioh/Documents/intro-data-science/crawler/data/vietnamnet.json " + file_name + " "
copy_operator = SSHOperator(
    ssh_hook=sshHook,
    task_id='save-to-hdfs',
    command=copy_command,
    dag=crawl_dag
)


start_task >> run_opetator >> copy_operator
