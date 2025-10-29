# Real Time EIS Pipeline

<!-- A comprehensive data pipeline that collects, cleans, validates, and visualizes economic data for real-time monitoring of Egypt's financial health.  -->

## Overview

The Economic Intelligence System (EIS) monitors and analyzes key economic indicators including:
- **USD ↔ EGP exchange rates** (daily)
- **Gold and silver prices** (daily, per troy ounce & per gram)
- **Economic indicators** (annual): Inflation, GDP growth, Unemployment
- **Stock market indices** (yearly): S&P 500, Dow Jones



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
