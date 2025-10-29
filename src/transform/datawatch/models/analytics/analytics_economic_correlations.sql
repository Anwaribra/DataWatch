{{ config(
    materialized='view',
    description='Correlation matrix between economic indicators, metals prices, and stock indices'
) }}

with fact_data as (
    select 
        date,
        gold_price_usd,
        silver_price_usd,
        usd_egp_rate,
        inflation_rate,
        gdp_growth_rate,
        unemployment_rate,
        sp500
    from {{ ref('fact_daily_metrics') }}
    where gold_price_usd is not null
        and silver_price_usd is not null
        and inflation_rate is not null
)

-- Calculate correlation matrix between different metrics
select
    'Gold vs Inflation' as metric_pair,
    corr(gold_price_usd, inflation_rate) as correlation
from fact_data

union all

select
    'Gold vs GDP Growth' as metric_pair,
    corr(gold_price_usd, gdp_growth_rate) as correlation
from fact_data

union all

select
    'Gold vs Unemployment' as metric_pair,
    corr(gold_price_usd, unemployment_rate) as correlation
from fact_data

union all

select
    'Gold vs S&P 500' as metric_pair,
    corr(gold_price_usd, sp500) as correlation
from fact_data

union all

select
    'Silver vs Inflation' as metric_pair,
    corr(silver_price_usd, inflation_rate) as correlation
from fact_data

union all

select
    'Exchange Rate vs Inflation' as metric_pair,
    corr(usd_egp_rate, inflation_rate) as correlation
from fact_data

