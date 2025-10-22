# Inventory-Management
A project that combines Docker containers and Apache Airflow orchestration to achieve automatic inventory management and sales reporting using Square's POS

## Disclaimer

This project is shared publicly for **educational and demonstration purposes**.  
It is intended to showcase concepts in inventory management systems, workflow automation, and system integration.  

To maintain security and protect sensitive configurations, only summaries and walkthroughs are provided.  

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
1. Before running Airflow in the CLI, the containers must be running in order to use the environment inside the container
2. Take a minute to inspect the dags folder. In it you will find more information about the necessary components for our dag scripts
3. On another tab, run the Airflow CLI. "docker compose exec airflow-scheduler" is the necessary command to tell docker to run Airflow commands inside the scheduler who is responsible for running the services:
   
    - Run this command to check existing dags in your dags folder: docker compose exec airflow-scheduler airflow dags list
    - Run this command to unpause the dags and begin scheduling: docker compose exec airflow-scheduler airflow dags unpause business_day_simulator
      
Under Tutorials/Airflow CLI, there is a list of other airflow commands for other services as well

4. Expected output for business_day_simulator:
    - creation of a CSV file with the corresponding date under logs folder (Sample output will be provided under logs_output)
    - email notifications being sent to the receiver Google email
    - logging information containing inventory deduction quantity and order_id for Square reference
  
5. The sales_report portion takes all the Order_id's from the CSV files, fetches the order's data to create an aggregation based on item and modifier for a corresponding date
6. Expected output for sales_report:
    - creation of a CSV file with the corresponding date under logs folder (Sample output will be provided under logs_output)
    - A summation of all the menu's items and its total revenue generated
    - A summation of all the modifiers used by items and its total revenue generated
    - A grand total of all the revenue generated for the corresponding date

## Performance Optimization
Major changes in structure and code logic were made to improve the performance of orchestration:

Version 1: Originally, one scheduled DAG run would take about 3 minutes to complete:
- API calls to deduct inventory were made per order, and CSV saves were per ingredient per order. Accumulation of network requests and I/O resulted in longer dag runs. Since catchup=True, the total time to complete ALL scheduled runs was amplified by the performance of a single scheduled run
- Had 5 PythonOperators (
  1. create csv
  2. send alert
  3. retrieve ingredients that needed restock and reorder
  4. save the restock log into the CSV
  5. simulate the business day )

Version 2: single scheduled runs would take around 2 minutes, 1 minute less than Version 1:
- From single calls to Batch calls were sent to Square whenever possible. This meant that creating orders and deducting inventory has to be stored in lists and dictionaries to later be sent to Square as batches. Some batch deductions were capped to the 100 limit so a separate for-loop was introduced to slice the batch into micro-batch sends.
- Incorporated batch saves to CSV as well. Introduced a counter to access timestamp element for logging order inventory deduction time based on order
- limited API calls to fetch latest order every time to only once per day by creating a Reference_id() class and then incrementing one to mimic static property
- compressed tasks from 5 to 3 PythonOperators (
  1. create csv
  2. send alert and manage restock into a single task
  3. simulate business day)

## Local runs
For analytical experimentation, It is crucial to observe data over a big time frame in large scales. Here's some of the insight that could be gained:
- Summaries over different time periods (daily, weekly, monthly, yearly, etc)
- Group By ingredients, line_item, modifiers
- Aggregation on ingredients, cost, revenue, and profit.

Simulator.py is a modified script of the Dag_Scheduler.
- It appends the deduction of inventory tracking in a single CSV file to eliminate the need of reading and merging CSV dataframes.
- runs 1000 orders instead of 100 daily
- starts at January 1 and ends at December 31
- produces around 365K orders, with a total number of rows reaching 1.4 million
- Does NOT make any API calls to Square so it saves a ton of time for generating random data

Since the file is too large to be uploaded, a link from Google Drive is pasted for downloading: https://drive.google.com/file/d/1BnTTYSdPfBc1GKIwabjC_2V7X52EpgAb/view?usp=sharing


