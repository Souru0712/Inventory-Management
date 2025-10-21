FROM apache/airflow:3.0.5-python3.11
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt