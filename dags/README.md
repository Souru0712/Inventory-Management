# For orchestration

Take a minute to inspect the dag scripts. Each dag object has a "start_date" 
  which determines the point at which the Scheduler should start

## Components:
catchup=True: as soon as the dags start running, it will begin backfilling until the current date
"schedule=@:" determines the frequency, so a daily schedule would increment every day until the current date
"max_active_runs=1": allows sequential task processing.
