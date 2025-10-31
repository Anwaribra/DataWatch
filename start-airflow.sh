#!/bin/bash

# Activate Airflow Virtual Environment
source ~/airflow-venv/bin/activate

# Make sure no Webserver is already running
echo "Killing running Airflow Webservers (if any)..."
sudo kill -9 $(lsof -t -i:8080) 2>/dev/null || true

# Remove stale PID file
rm -f ~/airflow/airflow-webserver.pid

# Initialize Airflow database if needed
echo "Checking Airflow database..."
airflow db check 2>/dev/null || airflow db init

echo "Starting Airflow Webserver..."
airflow webserver -p 8080 > ~/airflow/logs/webserver.log 2>&1 &
WEBSERVER_PID=$!
echo "Webserver started with PID: $WEBSERVER_PID"

sleep 5

echo "Starting Airflow Scheduler..."
airflow scheduler > ~/airflow/logs/scheduler.log 2>&1 &
SCHEDULER_PID=$!
echo "Scheduler started with PID: $SCHEDULER_PID"

echo "Airflow is running!"
echo "Webserver PID: $WEBSERVER_PID"
echo "Scheduler PID: $SCHEDULER_PID"
echo "Access Airflow UI at: http://localhost:8080"

# Wait for both processes
wait $WEBSERVER_PID $SCHEDULER_PID
