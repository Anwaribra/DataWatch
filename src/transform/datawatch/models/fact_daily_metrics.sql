{{ config(
    materialized='table',
    indexes=[
        {'columns': ['date_id'], 'type': 'btree'},
        {'columns': ['date'], 'type': 'btree'},
    ],
    unique_key=['date_id']
) }}

with exchange_rates as (
    select 
        date,
        usd_egp_rate
    from {{ ref('stg_exchange_rates') }}
),

metals as (
    select 
        date,
        gold_price_usd,
        silver_price_usd
    from {{ ref('stg_metals_prices') }}
),

economic_indicators as (
    select 
        date,
        inflation_rate,
        gdp_growth_rate,
        unemployment_rate
    from {{ ref('stg_economic_indicators') }}
),

stock_indices as (
    select 
        date,
        sp500
    from {{ ref('stg_stock_indices') }}
),

-- Get date dimension for joining
dates as (
    select 
        date_id,
        date
    from {{ ref('dim_date') }}
),

-- Combine metrics by date
combined_metrics as (
    select
        d.date_id,
        d.date,
        -- Exchange rates
        e.usd_egp_rate,
        -- Prices per troy ounce (USD)
        m.gold_price_usd,
        m.silver_price_usd,
        -- Prices per troy ounce (EGP) - calculated columns for performance
        -- NULL-safe calculations: only calculate if both source values exist
        case 
            when m.gold_price_usd is not null and e.usd_egp_rate is not null 
            then m.gold_price_usd * e.usd_egp_rate 
            else null 
        end as gold_price_egp,
        case 
            when m.silver_price_usd is not null and e.usd_egp_rate is not null 
            then m.silver_price_usd * e.usd_egp_rate 
            else null 
        end as silver_price_egp,
        -- Prices per gram (USD) - 1 troy ounce = 31.1035 grams
        m.gold_price_usd / 31.1035 as gold_price_usd_per_gram,
        m.silver_price_usd / 31.1035 as silver_price_usd_per_gram,
        -- Prices per gram (EGP) - NULL-safe calculations
        case 
            when m.gold_price_usd is not null and e.usd_egp_rate is not null 
            then (m.gold_price_usd * e.usd_egp_rate) / 31.1035 
            else null 
        end as gold_price_egp_per_gram,
        case 
            when m.silver_price_usd is not null and e.usd_egp_rate is not null 
            then (m.silver_price_usd * e.usd_egp_rate) / 31.1035 
            else null 
        end as silver_price_egp_per_gram,
        -- Economic indicators (annual data, forward-filled to daily)
        eco.inflation_rate,
        eco.gdp_growth_rate,
        eco.unemployment_rate,
        -- Stock market indices
        si.sp500
    from dates d
    left join exchange_rates e on d.date = e.date
    left join metals m on d.date = m.date
    left join economic_indicators eco on date_trunc('year', d.date) = date_trunc('year', eco.date)
    left join stock_indices si on d.date = si.date
)

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
    -- Economic indicators
    inflation_rate,
    gdp_growth_rate,
    unemployment_rate,
    -- Stock indices
    sp500
from combined_metrics
where gold_price_usd is not null 
   or silver_price_usd is not null
order by date


