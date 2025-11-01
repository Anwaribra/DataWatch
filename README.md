# Real Time EIS Pipeline

<!-- A comprehensive data pipeline that collects, cleans, validates, and visualizes economic data for real-time monitoring of Egypt's financial health.  -->

## Overview

The Economic Intelligence System (EIS) monitors and analyzes key economic indicators for Egypt's financial health.
The pipeline tracks **USD ↔ EGP exchange rates** (daily) and **gold and silver prices** (daily, per troy ounce & per gram).
Annual **economic indicators** include inflation, GDP growth, and unemployment rates sourced from the World Bank.
Yearly **stock market indices** include the S&P 500 and Dow Jones for global economic context.

## Pipeline Architecture

## Key Features

- ELT pipeline with star schema data warehouse design using PostgreSQL
- Multi-source data integration (Alpha Vantage, Yahoo Finance, World Bank API)
- dbt-powered SQL transformations with data lineage tracking
- Automated data quality validation with Soda Core (referential integrity, calculated columns, range validation)
- Daily orchestration via Apache Airflow with parallel extraction and retry logic
- Advanced analytics views (correlations, moving averages, daily returns, inflation impact analysis)
- Currency conversion (USD to EGP) and per-gram precious metals pricing (troy ounce conversion)
- Docker containerization for easy deployment and scaling




## Airflow DAG

The EIS pipeline is orchestrated using Apache Airflow and follows an ELT (Extract, Load, Transform) pattern:

![EIS Pipeline DAG](docs/eis_pipeline-graph.png)

## Data Warehouse ERD (Star Schema)

```mermaid
erDiagram
  DIM_DATE ||--o{ FACT_DAILY_METRICS : "has"

  DIM_DATE {
    int date_id PK 
    date date 
    int year
    int quarter
    int month
    int day
    int day_of_week
    boolean is_weekend
    int week
    string month_name
    string day_name
  }

  FACT_DAILY_METRICS {
    int date_id FK 
    date date 
    numeric gold_price_usd 
    numeric silver_price_usd 
    numeric usd_egp_rate 
    numeric gold_price_egp 
    numeric silver_price_egp 
    numeric gold_price_usd_per_gram 
    numeric silver_price_usd_per_gram 
    numeric gold_price_egp_per_gram 
    numeric silver_price_egp_per_gram 
    numeric inflation_rate 
    numeric gdp_growth_rate 
    numeric unemployment_rate
    numeric sp500
  }

  STG_EXCHANGE_RATES ||..o{ FACT_DAILY_METRICS : "feeds"
  STG_METALS_PRICES ||..o{ FACT_DAILY_METRICS : "feeds"
  STG_ECONOMIC_INDICATORS ||..o{ FACT_DAILY_METRICS : "feeds"
  STG_STOCK_INDICES ||..o{ FACT_DAILY_METRICS : "feeds"

  STG_EXCHANGE_RATES {
    date date PK
    numeric usd_egp_rate
    string metric_type
  }

  STG_METALS_PRICES {
    date date PK
    numeric gold_price_usd
    numeric silver_price_usd
    string source
  }

  STG_ECONOMIC_INDICATORS {
    date date PK
    numeric inflation_rate
    numeric gdp_growth_rate
    numeric unemployment_rate
    string source
  }

  STG_STOCK_INDICES {
    date date PK
    numeric sp500
  }
```
