{{ config(
    materialized='view',
    schema='analytics_lastyear',
    description='Moving averages (7-day and 30-day) for last year data only',
    tags=['analytics_lastyear', 'analytics']
) }}

with fact_data as (
    select 
        date,
        gold_price_usd,
        silver_price_usd,
        usd_egp_rate
    from {{ ref('fact_daily_metrics_lastyear') }}
    where gold_price_usd is not null
        and silver_price_usd is not null
        and usd_egp_rate is not null
)

select 
    date,
    gold_price_usd,
    silver_price_usd,
    usd_egp_rate,
    avg(gold_price_usd) over (
        order by date 
        rows between 6 preceding and current row
    ) as gold_ma_7d,
    avg(silver_price_usd) over (
        order by date 
        rows between 6 preceding and current row
    ) as silver_ma_7d,
    avg(usd_egp_rate) over (
        order by date 
        rows between 6 preceding and current row
    ) as exchange_rate_ma_7d,
    -- 30-day moving averages
    avg(gold_price_usd) over (
        order by date 
        rows between 29 preceding and current row
    ) as gold_ma_30d,
    avg(silver_price_usd) over (
        order by date 
        rows between 29 preceding and current row
    ) as silver_ma_30d,
    avg(usd_egp_rate) over (
        order by date 
        rows between 29 preceding and current row
    ) as exchange_rate_ma_30d
from fact_data
order by date

