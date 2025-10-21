from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
from sqlalchemy import create_engine
import subprocess
import json
import os


