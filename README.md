# Inventory-Management
A project that combines Docker containers and Apache Airflow orchestration to achieve automatic inventory management and sales reporting using Square's POS

## Disclaimer

This project is shared publicly for **educational and demonstration purposes**.  
It is intended to showcase concepts in inventory management systems, workflow automation, and system integration.  

To maintain security and protect sensitive configurations, only summaries and demonstrations are provided.  
A companion video is available to illustrate how the services run and interact.

You are welcome to **view and learn** from this project.  
However, please **do not copy, redistribute, or use this code in production or commercial environments** without explicit permission from the author.

## Walkthrough
1. A Square account needs to be created in order to retrieve the api_key and have access to the sandbox mode.
2. located in engineering/square/Setup.py, the python program creates all the necessary objects in Square to process the flow of inventory, including location, items, modifiers, inventory, and a reference_id to mimic ticket/order numbers.
3. The manual order randomizer is located in engineering/Simulator.py. Not only for real-life simulation, but also for having a variety of cases for deducting inventory, the large-scale simulator also proposes other roads like analytical analysis on sales and inventory throughout a given period in time.
4. For the orchestration part of the project, please check engineering/Dag_Scheduler and the dags folder. It is also crucial to follow the "Initiating Docker" header for initiating Docker before running Apache Airflow, which will do the orchestration.

## Initiating Docker
1. Install Docker Desktop.
2. Initiate docker on the terminal
    - Run this command to build the containers: docker compose up -d --build

      On the backend, the docker-compose.yml file is fetched and it scans through the services and builds containers.
      The "--build" is for including any Dockerfile references that may be called in any of your services

      The CLI will show "inventorymanagement" container up and running, but it can also be checked and seen in the Docker              Desktop 

The containers are for initiating airflow services which will be essential for orchestrating your workflow automatically. The containers will also create a remote airflow environment to allow running airflow commands in it, allowing which dags to run.

For more information on how to setup yaml files for Apache Airflow, visit the Apache Airflow's main website. They posted a sample yaml file (https://airflow.apache.org/docs/apache-airflow/3.1.0/docker-compose.yaml) that includes all the necessary and customizable credentials for initiating airflow through Docker containers

## Initiating Apache Airflow
1. make sure the containers are running in order to use the environment inside the container
2. Open another window on the terminal to start using Airflow.
    - "docker compose exec airflow-scheduler" is the necessary command to tell docker to run Airflow commands inside the                 scheduler who is responsible for running the services.
    - Run this command to check existing dags in your dags folder: docker compose exec airflow-scheduler airflow dags list

Under Tutorials/Airflow CLI, there is a list of other airflow commands for other services as well.

3. Take a minute to inspect the dag scripts.

Each dag object has a "start_date" which determines the date at which the Scheduler should start

catchup=True: as soon as the dags start running, it will begin backfilling until the current date
"schedule=@:" determines the frequency, so a daily schedule would increment every day until the current date
"max_active_runs=1": allows sequential task processing.















