# For orchestration

Take a minute to inspect the dag scripts. DAG objects are responsible for scheduling jobs. they require a dag_id in order to have a reference to it as well as tasks so that the DAG can orchestrate a workflow

## Components:
-"start_date": which determines the point at which the Scheduler should start
- "catchup=True": as soon as the dags start running, it will begin backfilling until the current date
- "schedule=@": determines the frequency that the DAG scheduler should run in and it splits the time between start_date and your current_date by the frequency, so a daily schedule would increment every day until the current date
- "max_active_runs=1": allows sequential task processing. This is only added to the business_day_simulator because it ensures inventory detection for the corresponding date before opening. If removed, the scheduler will run each task horizontally and will have the same scan result for all dates
- tasks need Operators. For python UDF's, a PythonOperator object needs to be created in order for the tasks to operate
- the double arrows determine the direction of the stream. So task 1 has to be completed before task 2, and task 2 has to be completed before task 3.


 
