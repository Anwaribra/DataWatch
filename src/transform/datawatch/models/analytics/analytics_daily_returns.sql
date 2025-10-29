{{ config(
    materialized='view',
    description='Daily returns (percentage changes) and volatility metrics for all price indicators'
) }}

with fact_data as (
    select 
        date,
        gold_price_usd,
        silver_price_usd,
        usd_egp_rate,
        gold_price_egp,
        silver_price_egp
    from {{ ref('fact_daily_metrics') }}
    where gold_price_usd is not null
        and silver_price_usd is not null
),

lagged_data as (
    select
        date,
        gold_price_usd,
        lag(gold_price_usd, 1) over (order by date) as gold_price_usd_prev,
        silver_price_usd,
        lag(silver_price_usd, 1) over (order by date) as silver_price_usd_prev,
        usd_egp_rate,
        lag(usd_egp_rate, 1) over (order by date) as usd_egp_rate_prev
    from fact_data
)

select 
    date,
    gold_price_usd,
    silver_price_usd,
    usd_egp_rate,
    -- Calculate daily returns
    case 
        when gold_price_usd_prev > 0 
        then ((gold_price_usd - gold_price_usd_prev) / gold_price_usd_prev) * 100 
        else null 
    end as gold_return_pct,
    case 
        when silver_price_usd_prev > 0 
        then ((silver_price_usd - silver_price_usd_prev) / silver_price_usd_prev) * 100 
        else null 
    end as silver_return_pct,
    case 
        when usd_egp_rate_prev > 0 
        then ((usd_egp_rate - usd_egp_rate_prev) / usd_egp_rate_prev) * 100 
        else null 
    end as exchange_rate_return_pct
from lagged_data
order by date
