# EIS - Data Warehouse Architecture

## Overview

EIS implements a **Star Schema** data warehouse on PostgreSQL using dbt for transformations. The system collects economic data from multiple sources, processes it through staging layers, and builds analytical views for insights.

### System Architecture

- **Raw Layer**: Python scripts fetch data from APIs (Alpha Vantage, Yahoo Finance, World Bank)
- **Staging Layer**: dbt models clean and normalize raw data
- **Dimensional Layer**: Date dimension for time-based analysis
- **Fact Layer**: Consolidated metrics combining financial and economic data
- **Analytics Layer**: Derived insights including correlations, returns, and moving averages

### Key Features

- Star schema design for fast analytical queries
- Multiple data sources integrated seamlessly
- Automatic currency conversion (USD to EGP)
- Per-gram pricing for precious metals (1 troy ounce = 31.1035 grams)
- Economic correlation analysis
- Inflation regime detection
- Time-based trend analysis


## Star Schema Design

The Star Schema consists of:
- **1 Dimension Table**: `dim_date` with temporal attributes
- **1 Fact Table**: `fact_daily_metrics` with all economic indicators

This design enables efficient joins and fast analytical queries by minimizing table joins and using denormalized fact data.

```mermaid
erDiagram
    dim_date ||--o{ fact_daily_metrics : "has"
    
    dim_date {
        date date PK
        date_id date PK
        year int
        quarter int
        month int
        day int
        day_of_week int
        is_weekend bool
        month_name string
        day_name string
    }
    
    fact_daily_metrics {
        date_id date FK
        date date
        gold_price_usd numeric
        silver_price_usd numeric
        gold_price_egp numeric
        silver_price_egp numeric
        gold_usd_per_gram numeric
        silver_usd_per_gram numeric
        usd_egp_rate numeric
        inflation_rate numeric
        gdp_growth_rate numeric
        unemployment_rate numeric
        egx30 numeric
        sp500 numeric
    }
```

