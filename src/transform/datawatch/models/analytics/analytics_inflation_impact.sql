{{ config(
    materialized='view',
    description='Impact of inflation on gold and silver prices - analyzes price performance during different inflation regimes'
) }}

with returns_data as (
    select 
        date,
        inflation_rate,
        gold_price_usd,
        silver_price_usd,
        usd_egp_rate,
        case 
            when lag(gold_price_usd, 1) over (order by date) > 0 
            then ((gold_price_usd - lag(gold_price_usd, 1) over (order by date)) / lag(gold_price_usd, 1) over (order by date)) * 100 
            else null 
        end as gold_return_pct,
        case 
            when lag(silver_price_usd, 1) over (order by date) > 0 
            then ((silver_price_usd - lag(silver_price_usd, 1) over (order by date)) / lag(silver_price_usd, 1) over (order by date)) * 100 
            else null 
        end as silver_return_pct
    from {{ ref('fact_daily_metrics') }}
    where gold_price_usd is not null
        and silver_price_usd is not null
        and inflation_rate is not null
),

inflation_regimes as (
    select 
        date,
        inflation_rate,
        gold_price_usd,
        silver_price_usd,
        gold_return_pct,
        silver_return_pct,
        case 
            when inflation_rate < 0 then 'Deflation'
            when inflation_rate < 2 then 'Low Inflation (0-2%)'
            when inflation_rate < 5 then 'Moderate Inflation (2-5%)'
            when inflation_rate < 10 then 'High Inflation (5-10%)'
            else 'Very High Inflation (>10%)'
        end as inflation_regime
    from returns_data
)

select 
    date,
    inflation_rate,
    inflation_regime,
    gold_price_usd,
    silver_price_usd,
    gold_return_pct,
    silver_return_pct,
    -- Calculate cumulative returns for each regime
    avg(gold_return_pct) over (
        partition by inflation_regime 
        order by date 
        rows between unbounded preceding and current row
    ) as cumulative_gold_return,
    avg(silver_return_pct) over (
        partition by inflation_regime 
        order by date 
        rows between unbounded preceding and current row
    ) as cumulative_silver_return
from inflation_regimes
order by date
