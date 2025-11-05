{{ config(
    materialized='table',
    schema='analytics_lastyear',
    indexes=[
        {'columns': ['date_id'], 'type': 'btree'},
        {'columns': ['date'], 'type': 'btree'},
    ],
    unique_key=['date_id'],
    tags=['analytics_lastyear']
) }}

select 
    date_id,
    date,
    -- Per troy ounce prices
    gold_price_usd,
    silver_price_usd,
    usd_egp_rate,
    gold_price_egp,
    silver_price_egp,
    -- Per gram prices (1 troy ounce = 31.1035 grams)
    gold_price_usd_per_gram,
    silver_price_usd_per_gram,
    gold_price_egp_per_gram,
    silver_price_egp_per_gram,

    inflation_rate,
    gdp_growth_rate,
    unemployment_rate,
    sp500
from {{ ref('fact_daily_metrics') }}
where extract(year from date) = 2025
order by date

